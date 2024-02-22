from rest_framework import serializers
from django.contrib.auth.models import User
from listing360.models import Property, District, Category, City, SelectOption, Field, SelectField, LongTextField, \
    DateField, IntegerField, ShortTextField, CategoryField


class PropertySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Property
        fields = ['id', 'user', 'title', 'description', 'type', 'status', 'is_active', 'is_available']
        read_only_fields = ['id', 'user', 'status']

    def create(self, validated_data):
        # L'utilisateur est ajouté dans la vue, pas ici
        return Property.objects.create(**validated_data)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'


class DateFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateField
        fields = ['id', 'minDate', 'maxDate']

class IntegerFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegerField
        fields = ['id', 'minValue', 'maxValue']

class SelectOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectOption
        fields = ['id', 'option_value', 'option_label']

class SelectFieldSerializer(serializers.ModelSerializer):
    options = SelectOptionSerializer(many=True, source='options')

    class Meta:
        model = SelectField
        fields = ['id', 'defaultValue', 'options']

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ['id', 'field_name', 'label', 'field_type']

class ShortTextFieldSerializer(serializers.ModelSerializer):
    field_name = serializers.CharField(source='base_field.field_name')
    label = serializers.CharField(source='base_field.label')

    class Meta:
        model = ShortTextField
        fields = ('id', 'field_name', 'label', 'max_length', 'placeholder', 'default_value', 'regex_pattern')

    def create(self, validated_data):
        field_data = validated_data.pop('base_field')
        field = Field.objects.create(**field_data)
        short_text_field = ShortTextField.objects.create(base_field=field, **validated_data)
        return short_text_field

    def update(self, instance, validated_data):
        field_data = validated_data.pop('base_field')
        Field.objects.filter(id=instance.base_field.id).update(**field_data)
        return super().update(instance, validated_data)

class LongTextFieldSerializer(serializers.ModelSerializer):
    field_name = serializers.CharField(source='base_field.field_name')
    label = serializers.CharField(source='base_field.label')
    # Ajoutez d'autres champs spécifiques à LongTextField si nécessaire

    class Meta:
        model = LongTextField
        fields = ('id', 'field_name', 'label', 'placeholder', 'rows', 'cols', 'maxLength', 'spellCheck')

    def create(self, validated_data):
        field_data = validated_data.pop('base_field')
        field = Field.objects.create(**field_data)
        long_text_field = LongTextField.objects.create(base_field=field, **validated_data)
        return long_text_field

    def update(self, instance, validated_data):
        field_data = validated_data.pop('base_field')
        Field.objects.filter(id=instance.base_field.id).update(**field_data)
        return super().update(instance, validated_data)

class LongTextFieldSerializer(serializers.ModelSerializer):
    field_name = serializers.CharField(source='base_field.field_name')
    label = serializers.CharField(source='base_field.label')
    # Ajoutez d'autres champs spécifiques à LongTextField si nécessaire

    class Meta:
        model = LongTextField
        fields = ('id', 'field_name', 'label', 'placeholder', 'rows', 'cols', 'maxLength', 'spellCheck')

    def create(self, validated_data):
        field_data = validated_data.pop('base_field')
        field = Field.objects.create(**field_data)
        long_text_field = LongTextField.objects.create(base_field=field, **validated_data)
        return long_text_field

    def update(self, instance, validated_data):
        field_data = validated_data.pop('base_field')
        Field.objects.filter(id=instance.base_field.id).update(**field_data)
        return super().update(instance, validated_data)

class DateFieldSerializer(serializers.ModelSerializer):
    field_name = serializers.CharField(source='base_field.field_name', required=True)
    label = serializers.CharField(source='base_field.label', required=True)

    class Meta:
        model = DateField
        fields = ('id', 'field_name', 'label', 'minDate', 'maxDate')

    def create(self, validated_data):
        field_data = validated_data.pop('base_field', {})
        field = Field.objects.create(**field_data)
        date_field = DateField.objects.create(base_field=field, **validated_data)
        return date_field

    def update(self, instance, validated_data):
        field_data = validated_data.pop('base_field')
        Field.objects.filter(id=instance.base_field.id).update(**field_data)
        return super().update(instance, validated_data)

class IntegerFieldSerializer(serializers.ModelSerializer):
    field_name = serializers.CharField(source='base_field.field_name', required=True)
    label = serializers.CharField(source='base_field.label', required=True)

    class Meta:
        model = IntegerField
        fields = ('id', 'field_name', 'label', 'minValue', 'maxValue')

    def create(self, validated_data):
        field_data = validated_data.pop('base_field', {})
        field = Field.objects.create(**field_data)
        integer_field = IntegerField.objects.create(base_field=field, **validated_data)
        return integer_field

    def update(self, instance, validated_data):
        field_data = validated_data.pop('base_field')
        Field.objects.filter(id=instance.base_field.id).update(**field_data)
        return super().update(instance, validated_data)

class SelectOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectOption
        fields = ['id', 'label', 'value']

class SelectFieldSerializer(serializers.ModelSerializer):
    options = SelectOptionSerializer(many=True)
    field_name = serializers.CharField(source='base_field.field_name')
    label = serializers.CharField(source='base_field.label')

    class Meta:
        model = SelectField
        fields = ['id', 'field_name', 'label', 'options']

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        base_field_data = validated_data.pop('base_field')
        field_name = base_field_data.get('field_name')
        label = base_field_data.get('label')

        # Créer le BaseField
        base_field = Field.objects.create(field_name=field_name, label=label)

        # Créer le SelectField avec le BaseField créé
        select_field = SelectField.objects.create(base_field=base_field, **validated_data)

        # Créer les options de SelectField
        for option_data in options_data:
            SelectOption.objects.create(select_field=select_field, **option_data)

        return select_field

    def update(self, instance, validated_data):
        options_data = validated_data.pop('options', [])
        base_field_data = validated_data.pop('base_field', {})

        # Mise à jour du BaseField
        Field.objects.filter(id=instance.base_field.id).update(**base_field_data)

        # Mise à jour de l'instance SelectField
        instance.label = validated_data.get('label', instance.label)
        instance.save()

        # Mise à jour des options
        existing_option_ids = [option.id for option in instance.options.all()]
        for option_data in options_data:
            option_id = option_data.get('id', None)
            if option_id in existing_option_ids:
                existing_option_ids.remove(option_id)
                SelectOption.objects.filter(id=option_id).update(**option_data)
            else:
                SelectOption.objects.create(select_field=instance, **option_data)

        # Supprimer les options qui n'ont pas été incluses dans la requête
        SelectOption.objects.filter(id__in=existing_option_ids).delete()

        return instance

class CategoryFieldSerializer(serializers.ModelSerializer):
    field = serializers.PrimaryKeyRelatedField(queryset=Field.objects.all(), write_only=True)

    class Meta:
        model = CategoryField
        fields = ['id', 'field', 'is_required']

    def create(self, validated_data):
        category_field = CategoryField.objects.create(**validated_data)
        return category_field

class CategorySerializer(serializers.ModelSerializer):
    category_fields = CategoryFieldSerializer( many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'application_type', 'category_fields']

    def create(self, validated_data):
        print(validated_data)
        category_fields_data = validated_data.pop('category_fields')
        category = Category()
        category.name = validated_data.get('name')
        category.application_type = validated_data.get('application_type')
        category.save()
        print(category_fields_data)
        for field_data in category_fields_data:
            CategoryField.objects.create(category=category, **field_data)
        return category

    def update(self, instance, validated_data):
        print("Données validées pour la mise à jour :", validated_data)
        category_fields_data = validated_data.pop('category_fields', [])

        # Mise à jour des attributs simples de Category
        instance.name = validated_data.get('name', instance.name)
        instance.application_type = validated_data.get('application_type', instance.application_type)
        instance.save()


        instance.category_fields.all().delete()

        # Création des nouveaux CategoryField à partir des données fournies
        for field_data in category_fields_data:
            CategoryField.objects.create(category=instance, **field_data)

        return instance


class DynamicFieldSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()

    class Meta:
        model = Field
        fields = ['id', 'field_name', 'label', 'field_type', 'details']

    def get_details(self, obj):
        # Détermine le type de champ et sérialise les données en conséquence
        if obj.field_type == 'text_long':
            detail_instance = LongTextField.objects.get(base_field=obj)
            return LongTextFieldSerializer(detail_instance).data
        elif obj.field_type == 'date':
            detail_instance = DateField.objects.get(base_field=obj)
            return DateFieldSerializer(detail_instance).data
        elif obj.field_type == 'integer':
            detail_instance = IntegerField.objects.get(base_field=obj)
            return IntegerFieldSerializer(detail_instance).data
        elif obj.field_type == 'select':
            detail_instance = SelectField.objects.get(base_field=obj)
            return SelectFieldSerializer(detail_instance, context=self.context).data
        elif obj.field_type == 'text_short':
            detail_instance = ShortTextField.objects.get(base_field=obj)
            return ShortTextFieldSerializer(detail_instance).data
        else:
            return {}
