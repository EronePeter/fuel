# Generated by Django 4.2.4 on 2023-08-29 14:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_fuellitre_fuel_litres_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='litresbeforenexttopup',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]