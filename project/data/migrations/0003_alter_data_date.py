# Generated by Django 4.1.5 on 2023-02-01 13:19

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0002_data_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="data",
            name="date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
