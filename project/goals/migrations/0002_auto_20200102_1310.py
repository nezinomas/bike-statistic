# Generated by Django 3.0.1 on 2020-01-02 11:10

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("goals", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="goal",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="goals",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="goal",
            name="year",
            field=models.IntegerField(
                validators=[
                    django.core.validators.MinValueValidator(2000),
                    django.core.validators.MaxValueValidator(2050),
                ]
            ),
        ),
        migrations.AlterUniqueTogether(
            name="goal",
            unique_together={("user", "year")},
        ),
    ]
