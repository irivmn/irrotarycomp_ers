# Generated by Django 3.2.13 on 2022-06-14 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ERS', '0007_cd26_airend_data_rated'),
    ]

    operations = [
        migrations.AddField(
            model_name='cd26_airend_data_rated',
            name='Max',
            field=models.FloatField(default=0),
        ),
    ]
