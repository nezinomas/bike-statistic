# Generated by Django 4.1.5 on 2023-01-16 12:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_auto_20210420_1508"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="first name"
            ),
        ),
    ]
