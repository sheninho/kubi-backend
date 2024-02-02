from django.contrib import admin
from .models import (
    Myuser, VerificationCode, Category, City, District, Property, Sale, Rental,
    Image, Field, LongTextField, DateField, IntegerField, SelectField, SelectOption,
    SelectFieldDefaultValue, ShortTextField, PropertyValue, Offer
)

# Enregistrement des modèles simples
admin.site.register(Myuser)
admin.site.register(VerificationCode)
admin.site.register(Category)
admin.site.register(City)
admin.site.register(District)
admin.site.register(Property)
admin.site.register(Sale)
admin.site.register(Rental)
admin.site.register(Image)
admin.site.register(SelectOption)
admin.site.register(SelectFieldDefaultValue)
admin.site.register(Offer)

# Pour les modèles avec des champs génériques ou des relations complexes,
# vous pouvez créer des classes d'administration personnalisées.


class LongTextFieldAdmin(admin.ModelAdmin):
    list_display = ('field_name', 'label', 'placeholder', 'maxLength')

admin.site.register(LongTextField, LongTextFieldAdmin)

class DateFieldAdmin(admin.ModelAdmin):
    list_display = ('field_name', 'label', 'minDate', 'maxDate')

admin.site.register(DateField, DateFieldAdmin)

class IntegerFieldAdmin(admin.ModelAdmin):
    list_display = ('field_name', 'label', 'minValue', 'maxValue')

admin.site.register(IntegerField, IntegerFieldAdmin)

class SelectFieldAdmin(admin.ModelAdmin):
    list_display = ('field_name', 'label', 'defaultValue')

admin.site.register(SelectField, SelectFieldAdmin)

class ShortTextFieldAdmin(admin.ModelAdmin):
    list_display = ('field_name', 'label', 'max_length', 'default_value')

admin.site.register(ShortTextField, ShortTextFieldAdmin)

class PropertyValueAdmin(admin.ModelAdmin):
    list_display = ('property', 'field', 'value')
    list_filter = ('property', 'field')

admin.site.register(PropertyValue, PropertyValueAdmin)

# Vous pouvez ajouter des classes d'administration supplémentaires si nécessaire
# pour personnaliser l'affichage et la gestion de vos modèles dans l'interface d'administration.
