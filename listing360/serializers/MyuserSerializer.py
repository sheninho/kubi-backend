from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ObjectDoesNotExist
from listing360.models import VerificationCode, Myuser
from django.core.mail import send_mail
import random
# from ..tasks import send_verification_email

class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['phone_number', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number')  # Phone number is stored in username
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        password = validated_data.pop('password')
        try:
            user = User.objects.get(username=phone_number)
            # Vérifier si l'utilisateur existant est validé
            if user.myuser.activated:
                raise serializers.ValidationError({'error': 'Ce numéro de téléphone est déjà utilisé.'})
            else:
                # Supprimer l'utilisateur non validé
                user.delete()
        except ObjectDoesNotExist:
            pass
        user = User(username=phone_number)
        user.set_password(password)
        user.save()
        myuser=Myuser.objects.create(user=user, first_name=first_name, last_name=last_name, activated=False)
        # Générer et envoyer le code de vérification
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        VerificationCode.create(myuser=myuser)
        return user
    def to_representation(self, instance):
        """
        Surchargez la représentation de l'instance pour inclure le time_left.
        """
        representation = super(UserSerializer, self).to_representation(instance)
        representation['time_left'] = getattr(instance, 'time_left', 0)  # Ajoutez time_left à la réponse
        return representation


class AccountActivationSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField()

    def validate(self, data):
        phone_number = data.get('phone_number')
        code = data.get('code')

        # Vérifier si l'utilisateur existe
        try:
            user = User.objects.get(username=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError({'error': 'Numéro de téléphone invalide.'})

        # Vérifier si le code est correct
        try:
            verification_entry = VerificationCode.objects.get(myuser=user.myuser, code=code)
        except VerificationCode.DoesNotExist:
            raise serializers.ValidationError({'error': 'Code de vérification invalide.'})

        # Vérifier si le compte n'est pas déjà activé
        if user.myuser.activated:
            raise serializers.ValidationError({'error': 'Ce compte est déjà activé.'})

        return data

    def save(self, **kwargs):
        phone_number = self.validated_data.get('phone_number')
        user = User.objects.get(username=phone_number)

        # Activer le compte
        myuser = user.myuser
        myuser.activated = True
        myuser.save()

        # Vous pouvez également supprimer le code de vérification ici si nécessaire
        VerificationCode.objects.filter(myuser=myuser).delete()

        return user


class VerificationCodeSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(slug_field='user__username', queryset=Myuser.objects.all())

    class Meta:
        model = VerificationCode
        fields = ['myuser', 'code']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Valider les données avec la méthode parent
        data = super().validate(attrs)

        # Récupérer l'utilisateur
        user = User.objects.get(username=attrs['username'])

        # Vérifier si l'utilisateur est activé et validé
        if not user.myuser.activated or not user.myuser.validated:
            raise AuthenticationFailed('Votre compte n\'est pas activé ou validé.')

        return data