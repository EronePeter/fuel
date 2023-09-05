# Generated by Django 4.2.4 on 2023-08-28 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_sale_litres_per_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='total_sold_litres',
            field=models.DecimalField(decimal_places=4, max_digits=9, verbose_name='Current reading of sold fuel litres'),
        ),
    ]
