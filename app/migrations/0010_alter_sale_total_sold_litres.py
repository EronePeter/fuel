# Generated by Django 4.2.4 on 2023-08-31 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_sale_total_sold_litres'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='total_sold_litres',
            field=models.DecimalField(decimal_places=4, max_digits=9, verbose_name='Total consumed/sold ltrs'),
        ),
    ]