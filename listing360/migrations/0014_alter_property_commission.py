# Generated by Django 5.0 on 2024-02-08 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listing360', '0013_category_application_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='commission',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
    ]