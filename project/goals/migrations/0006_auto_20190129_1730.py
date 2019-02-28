# Generated by Django 2.1.4 on 2019-01-29 15:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0005_auto_20190129_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='distance',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(100), django.core.validators.MaxValueValidator(20000)]),
        ),
        migrations.AlterField(
            model_name='goal',
            name='year',
            field=models.IntegerField(unique=True, validators=[django.core.validators.MinValueValidator(2000), django.core.validators.MaxValueValidator(2050)]),
        ),
    ]