# Generated by Django 5.0 on 2024-01-11 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listing360', '0006_property_creation_step_property_is_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='nom',
            field=models.CharField(default='False', max_length=100),
        ),
        migrations.AddField(
            model_name='myuser',
            name='prenom',
            field=models.CharField(default='False', max_length=100),
        ),
    ]
