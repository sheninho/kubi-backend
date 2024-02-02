import random

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
import datetime

class Myuser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    activated = models.BooleanField(default=False)
    validated = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.first_name} {self.last_name}"

class VerificationCode(models.Model):
    myuser = models.ForeignKey(Myuser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_expired(self):
        # Le code expire après 1 heure (ou le délai que vous souhaitez)
        return self.created_at + datetime.timedelta(minutes=5) < timezone.now()

    @classmethod
    def create(cls, myuser):
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        verification_code = cls(
            myuser=myuser,
            code=code,
            created_at=timezone.now()
        )
        verification_code.save()
        send_mail(
            'Votre code de vérification',
            f'Votre code de vérification est: {code}',
            'msakande21@gmail.com',
            ['shunikiema@gmail.com',],
            fail_silently=False,
        )
        return verification_code


# Modèle pour les catégories de propriétés
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Association entre les catégories et leurs caractéristiques
class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='districts')

    def __str__(self):
        return f"{self.name}, {self.city.name}"



# Modèle pour les propriétés immobilières
class Property(models.Model):
    SALE = 'Sale'
    RENT = 'Rent'
    PROPERTY_TYPES = [
        (SALE, 'Sale'),
        (RENT, 'Rent'),
    ]
    CREATION_STEP_CHOICES = [
        ('basic_info', 'Basic Information'),
        ('category_district', 'Category and District'),
        ('features', 'Features'),
        ('images', 'Images'),
        ('review', 'Review'),
    ]

    STATUS_VALIDATED = 'validated'
    STATUS_REFUSED = 'refused'
    STATUS_PENDING = 'pending'
    STATUS_CHOICES = [
        (STATUS_VALIDATED, 'Validated'),
        (STATUS_REFUSED, 'Refused'),
        (STATUS_PENDING, 'Pending'),
    ]

    user = models.ForeignKey(Myuser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    type = models.CharField(max_length=100, choices=PROPERTY_TYPES)  # Exemple: À Vendre, À Louer
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=STATUS_PENDING)
    creation_step = models.CharField(
        max_length=20,
        choices=CREATION_STEP_CHOICES,
        default='basic_info'
    )
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    commission = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Sale(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    # ...

class Rental(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    # ...

class Image(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.property.title} - {self.description[:50]}"

# Association entre les propriétés et leurs caractéristiques spécifiques
class Field(models.Model):
    categories = models.ManyToManyField(Category)
    field_name = models.CharField(max_length=100, unique=True)  # Nom unique du champ
    label = models.CharField(max_length=100)  # Nom d'appellation pour l'affichage
    field_type = models.CharField(max_length=100, blank=True, editable=False)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.label} ({self.field_name})"

class LongTextField(Field):
    placeholder = models.CharField(max_length=255, blank=True, null=True)
    rows = models.PositiveIntegerField(default=4)
    cols = models.PositiveIntegerField(default=50)
    maxLength = models.PositiveIntegerField(null=True, blank=True)
    required = models.BooleanField(default=False)
    spellCheck = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.field_type = 'text_long'
        super(LongTextField, self).save(*args, **kwargs)

    def __str__(self):
        return f"{super().label} ({super().field_name})"

class DateField(Field):
    required = models.BooleanField(default=False)
    minDate = models.DateField(null=True, blank=True)
    maxDate = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.field_type = 'date'
        super(DateField, self).save(*args, **kwargs)

    def __str__(self):
        return f"{super().label} ({super().field_name})"

class IntegerField(Field):
    required = models.BooleanField(default=False)
    minValue = models.IntegerField(null=True, blank=True)
    maxValue = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.field_type = 'integer'
        super(IntegerField, self).save(*args, **kwargs)

    def __str__(self):
        return f"{super.label} ({super.field_name})"

class SelectField(Field):
    required = models.BooleanField(default=False)
    defaultValue = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.field_type = 'select'
        super(SelectField, self).save(*args, **kwargs)

    def __str__(self):
        return f"{super.label} ({super.field_name})"

class SelectOption(models.Model):
    select_field = models.ForeignKey(SelectField, related_name='options', on_delete=models.CASCADE)
    option_value = models.CharField(max_length=100)
    option_label = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.select_field.label} - {self.option_label}"

# Ajoutez un nouveau champ pour la valeur par défaut qui fait référence à SelectOption
class SelectFieldDefaultValue(models.Model):
    select_field = models.OneToOneField(SelectField, on_delete=models.CASCADE)
    default_option = models.ForeignKey(SelectOption, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Default for {self.select_field.label}: {self.default_option.option_label}"


class ShortTextField(Field):
    max_length = models.PositiveIntegerField(default=255)
    required = models.BooleanField(default=False)  # Si le champ est obligatoire
    placeholder = models.CharField(max_length=255, blank=True, null=True)  # Texte indicatif
    default_value = models.CharField(max_length=255, blank=True, null=True)  # Valeur par défaut
    regex_pattern = models.CharField(max_length=255, blank=True, null=True)  # Validation par regex

    def save(self, *args, **kwargs):
        self.field_type = 'text_short'
        super(ShortTextField, self).save(*args, **kwargs)

    def __str__(self):
        return f"{super.label} ({super.field_name})"

class PropertyValue(models.Model):
    property = models.ForeignKey(Property, related_name='property_values', on_delete=models.CASCADE)
    field = GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    value = models.TextField()

    def __str__(self):
        return f"{self.field.name}: {self.value}"

# Vous pouvez étendre ce fichier avec d'autres modèles selon vos besoins.
class Offer(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey(Myuser, on_delete=models.CASCADE)
    message = models.TextField()
    is_accepted = models.BooleanField(default=False)  # Si l'offre est acceptée ou non
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Offer of {self.offer_amount} on {self.property.title}"