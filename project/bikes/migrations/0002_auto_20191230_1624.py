# Generated by Django 3.0.1 on 2019-12-30 14:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("bikes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="bike",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bikes",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="bike",
            name="short_name",
            field=models.CharField(max_length=20),
        ),
        migrations.AlterUniqueTogether(
            name="bike",
            unique_together={("user", "short_name")},
        ),
    ]
