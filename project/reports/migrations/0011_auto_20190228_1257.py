# Generated by Django 2.1.7 on 2019-02-28 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0010_auto_20190129_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='temperature',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
