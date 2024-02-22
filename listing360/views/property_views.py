from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated

from ..models import District, Property, Category, City, Field, Myuser, CategoryField, ShortTextField, LongTextField, \
    SelectField, DateField, IntegerField
from ..serializers.PropertySerializer import PropertySerializer, DistrictSerializer, CategorySerializer, CitySerializer, \
    FieldSerializer, DynamicFieldSerializer, ShortTextFieldSerializer, LongTextFieldSerializer, SelectFieldSerializer, \
    DateFieldSerializer, IntegerFieldSerializer


# from .serializers import PropertySerializer

class CreatePropertyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        myuser_instance = get_object_or_404(Myuser, user=request.user)
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            property_instance = serializer.save(user=myuser_instance)  # Associez l'utilisateur à la propriété
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class CityListCreateView(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class CityRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class DistrictListCreateView(generics.ListCreateAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

class DistrictRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

class PropertyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

class CategoriesByPropertyTypeView(APIView):
    def get(self, request):
        property_type = request.query_params.get('property_type')

        # Vérifier si le type de propriété est valide
        if property_type not in ['sale', 'rent']:
            return Response({'error': 'Type de propriété invalide.'}, status=400)

        # Filtrer les catégories en fonction du type de propriété
        if property_type == 'sale':
            categories = Category.objects.filter(application_type__in=['sale', 'both'])
        elif property_type == 'rent':
            categories = Category.objects.filter(application_type__in=['rent', 'both'])

        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CityDistrictsListView(APIView):
    """
    View to list all cities and their associated districts.
    """

    def get(self, request, *args, **kwargs):
        # Récupérer toutes les villes
        cities = City.objects.all()

        # Préparer la réponse
        response_data = []

        for city in cities:
            # Récupérer les districts associés à la ville
            districts = District.objects.filter(city=city)

            # Sérialiser les données de la ville
            city_data = CitySerializer(city).data

            # Sérialiser les données des districts
            district_data = DistrictSerializer(districts, many=True).data

            # Ajouter les districts à la réponse de la ville
            city_data['districts'] = district_data

            # Ajouter la ville et ses districts à la réponse globale
            response_data.append(city_data)

        return Response(response_data)




class PropertyUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, property_id):
        # Trouvez l'instance de la propriété

        myuser_instance = get_object_or_404(Myuser, user=request.user)
        property_instance = Property.objects.filter(id=property_id, user=myuser_instance).first()
        if not property_instance:
            return Response({'error': 'Propriété non trouvée.'}, status=status.HTTP_404_NOT_FOUND)

        # Mettez à jour l'instance avec les données fournies
        serializer = PropertySerializer(property_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PropertyCategoryFieldsView(APIView):
    def get(self, request, property_id):
        # Trouver la propriété par son ID
        property_instance = Property.objects.get(id=property_id)
        # Obtenir la catégorie de la propriété
        category = property_instance.category

        # Trouver tous les CategoryField associés à cette catégorie
        category_fields = CategoryField.objects.filter(category=category)

        # Récupérer les instances de Field associées
        fields = [cf.field for cf in category_fields]

        # Sérialiser les champs en utilisant DynamicFieldSerializer
        serializer = DynamicFieldSerializer(fields, many=True, context={'request': request})

        return Response(serializer.data)


class ShortTextFieldListCreateAPIView(generics.ListCreateAPIView):
    queryset = ShortTextField.objects.all()
    serializer_class = ShortTextFieldSerializer

class ShortTextFieldRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShortTextField.objects.all()
    serializer_class = ShortTextFieldSerializer

class LongTextFieldListCreateAPIView(generics.ListCreateAPIView):
    queryset = LongTextField.objects.all()
    serializer_class = LongTextFieldSerializer

class LongTextFieldRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LongTextField.objects.all()
    serializer_class = LongTextFieldSerializer

class DateFieldListCreateAPIView(generics.ListCreateAPIView):
    queryset = DateField.objects.all()
    serializer_class = DateFieldSerializer

class DateFieldRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DateField.objects.all()
    serializer_class = DateFieldSerializer

class IntegerFieldListCreateAPIView(generics.ListCreateAPIView):
    queryset = IntegerField.objects.all()
    serializer_class = IntegerFieldSerializer

class IntegerFieldRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = IntegerField.objects.all()
    serializer_class = IntegerFieldSerializer

class SelectFieldListCreateAPIView(generics.ListCreateAPIView):
    queryset = SelectField.objects.all()
    serializer_class = SelectFieldSerializer

class SelectFieldRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SelectField.objects.all()
    serializer_class = SelectFieldSerializer

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    def post(self, request, *args, **kwargs):
        print("Données de la requête POST :", request.data)
        return super().post(request, *args, **kwargs)

class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def put(self, request, *args, **kwargs):
        print("Données de la requête PUT :", request.data)
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        print("Données de la requête PATCH :", request.data)
        return super().patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        print("Requête DELETE pour l'ID :", kwargs.get('pk'))
        return super().delete(request, *args, **kwargs)


class FieldListView(ListAPIView):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer