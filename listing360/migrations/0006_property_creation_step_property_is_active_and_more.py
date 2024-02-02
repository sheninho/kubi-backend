# Generated by Django 5.0 on 2024-01-06 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listing360', '0005_city_rename_client_verificationcode_myuser_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='creation_step',
            field=models.CharField(choices=[('basic_info', 'Basic Information'), ('category_district', 'Category and District'), ('features', 'Features'), ('images', 'Images'), ('review', 'Review')], default='basic_info', max_length=20),
        ),
        migrations.AddField(
            model_name='property',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='property',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='status',
            field=models.CharField(choices=[('validated', 'Validated'), ('refused', 'Refused'), ('pending', 'Pending')], default='pending', max_length=100),
        ),
    ]