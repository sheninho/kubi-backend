from django.contrib import admin
from .models import (
    Myuser, VerificationCode, Category, City, District, Property, Sale, Rental,
    Image, Field, LongTextField, DateField, IntegerField, SelectField, SelectOption,
    SelectFieldDefaultValue, ShortTextField, PropertyValue, Offer, CategoryField
)

# Inline pour les types de champs spécifiques
class LongTextFieldInline(admin.StackedInline):
    model = LongTextField
    can_delete = False
    verbose_name_plural = 'Long Text Fields'
    fk_name = 'base_field'

class DateFieldInline(admin.StackedInline):
    model = DateField
    can_delete = False
    verbose_name_plural = 'Date Fields'
    fk_name = 'base_field'

class IntegerFieldInline(admin.StackedInline):
    model = IntegerField
    can_delete = False
    verbose_name_plural = 'Integer Fields'
    fk_name = 'base_field'

class SelectOptionInline(admin.TabularInline):
    model = SelectOption
    can_delete = False
    verbose_name_plural = 'Select Options'
    fk_name = 'base_field'

class SelectFieldInline(admin.StackedInline):
    model = SelectField
    can_delete = False
    verbose_name_plural = 'Select Fields'
    fk_name = 'base_field'
    inlines = [SelectOptionInline]

class ShortTextFieldInline(admin.StackedInline):
    model = ShortTextField
    can_delete = False
    verbose_name_plural = 'Short Text Fields'
    fk_name = 'base_field'

# Admin pour Field avec inlines pour chaque type de champ spécifique
class FieldAdmin(admin.ModelAdmin):
    list_display = ('field_name', 'label', 'field_type')
    inlines = [LongTextFieldInline, DateFieldInline, IntegerFieldInline, SelectFieldInline, ShortTextFieldInline]

admin.site.register(Field, FieldAdmin)

# Inline pour CategoryField dans CategoryAdmin
class CategoryFieldInline(admin.TabularInline):
    model = CategoryField
    extra = 1

# Admin pour Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'application_type')
    list_filter = ('application_type',)
    search_fields = ('name',)
    inlines = [CategoryFieldInline]

admin.site.register(Category, CategoryAdmin)

# Admin pour les autres modèles
admin.site.register(Myuser)
admin.site.register(VerificationCode)
admin.site.register(City)
admin.site.register(District)
admin.site.register(Property)
admin.site.register(Sale)
admin.site.register(Rental)
admin.site.register(Image)
admin.site.register(SelectOption)
admin.site.register(SelectFieldDefaultValue)
admin.site.register(Offer)

# Admin pour PropertyValue
class PropertyValueAdmin(admin.ModelAdmin):
    list_display = ('property', 'field', 'value')
    list_filter = ('property', 'field')

admin.site.register(PropertyValue, PropertyValueAdmin)
