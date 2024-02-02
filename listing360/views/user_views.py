from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from
from listing360.models import Myuser, VerificationCode
from listing360.serializers.MyuserSerializer import  AccountActivationSerializer, UserSerializer, \
    CustomTokenObtainPairSerializer
import random
from django.utils import timezone
import datetime
import urllib.parse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActivateAccountView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AccountActivationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Compte activé avec succès."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TimeRemainingView(APIView):
    def get(self, request, *args, **kwargs):
        phone_number = request.query_params.get('phone_number')

        decoded_phone_number = urllib.parse.unquote(phone_number).replace(' ', '+')
        try:
            user = User.objects.get(username=decoded_phone_number)
            last_code = VerificationCode.objects.filter(myuser=user.myuser).order_by('-created_at').first()

            if last_code:
                time_remaining = max(0, (last_code.created_at + datetime.timedelta(minutes=2) - timezone.now()).total_seconds())
                return Response({"time_remaining": time_remaining})
            return Response({"time_remaining": 0})
        except User.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé"}, status=404)

class ResendCodeView(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')

        try:
            user = User.objects.get(username=phone_number)
            verification_code = VerificationCode.create(user.myuser)

            return Response({"message": "Code de vérification envoyé."})
        except User.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé"}, status=404)
class VerifyCodeView(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')

        try:
            user = User.objects.get(username=phone_number)
            verification_code = VerificationCode.objects.get(myuser=user.myuser, code=code)

            if verification_code and not verification_code.is_expired:
                return Response({"message": "Le code de vérification est correct."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Code de vérification incorrect ou expiré."}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)

class ChangePasswordView(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        new_password = request.data.get('new_password')

        try:
            user = User.objects.get(username=phone_number)
            user.set_password(new_password)
            user.save()

            return Response({"message": "Mot de passe mis à jour avec succès."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class TokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

# class LoginView(TokenObtainPairView):
#     def post(self, request, *args, **kwargs):
#         phone_number = request.data.get('phone_number')
#         password = request.data.get('password')
#
#         # Afficher les données de connexion pour le débogage
#         print(f"Tentative de connexion pour le numéro de téléphone: {phone_number}")
#
#         # Authentifier l'utilisateur
#         user = authenticate(username=phone_number, password=password)
#         if not user:
#             print("Échec de l'authentification - utilisateur non trouvé ou mot de passe incorrect")
#             return Response({"error": "Numéro de téléphone ou mot de passe incorrect."}, status=status.HTTP_401_UNAUTHORIZED)
#
#         if not user.is_active:
#             print("Échec de l'authentification - compte utilisateur désactivé")
#             return Response({"error": "Compte désactivé."}, status=status.HTTP_401_UNAUTHORIZED)
#
#         serializer = self.get_serializer(data=request.data)
#
#         try:
#             serializer.is_valid(raise_exception=True)
#         except TokenError as e:
#             print(f"Erreur de token: {e.args[0]}")
#             raise InvalidToken({"error": "Erreur lors de la création du token."})
#
#         print("Connexion réussie - Token créé")
#         return Response(serializer.validated_data, status=status.HTTP_200_OK)

class UserLogoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Recherche du token et ajout à la liste noire pour le désactiver
            token = OutstandingToken.objects.get(token=request.auth)
            BlacklistedToken.objects.create(token=token)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)