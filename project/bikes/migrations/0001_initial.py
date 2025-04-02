# Generated by Django 3.0.1 on 2019-12-23 09:43

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('full_name', models.CharField(blank=True, max_length=150)),
                ('short_name', models.CharField(max_length=20, unique=True)),
                ('slug', models.SlugField(editable=False)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, validators=[django.core.validators.MaxLengthValidator(99), django.core.validators.MinLengthValidator(3)])),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ComponentStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('brand', models.CharField(blank=True, max_length=254)),
                ('bike', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bikes', to='bikes.Bike')),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='components', to='bikes.Component')),
            ],
            options={
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='BikeInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('component', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=254)),
                ('bike', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bike_info', to='bikes.Bike')),
            ],
            options={
                'ordering': ['component'],
            },
        ),
    ]
