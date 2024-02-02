from rest_framework import serializers
from django.contrib.auth.models import User
from listing360.models import Property, District, Category, City, SelectOption, Field


class PropertySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Property
        fields = ['id', 'user', 'title', 'description', 'type', 'status', 'district', 'category', 'is_active', 'is_available']
        read_only_fields = ['id', 'user', 'status']

    def create(self, validated_data):
        # L'utilisateur est ajouté dans la vue, pas ici
        return Property.objects.create(**validated_data)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'


class SelectOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectOption
        fields = ['option_value', 'option_label']

class FieldSerializer(serializers.ModelSerializer):
    options = SelectOptionSerializer(many=True, read_only=True, source='selectfield_options')

    class Meta:
        model = Field
        fields = ['field_name', 'label', 'field_type', 'options']
        depth = 1


