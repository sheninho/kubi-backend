# Generated by Django 5.0 on 2024-01-11 22:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listing360', '0008_alter_myuser_nom_alter_myuser_prenom'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='nom',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='prenom',
        ),
    ]