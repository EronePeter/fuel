from django.db import models
from django.utils import timezone
from datetime import date
from django.conf import settings


class Common(models.Model):
    price_per_litre = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        abstract = True


class Sale(Common):
    litres_per_day = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True) # 6, 3
    date = models.DateTimeField(default=timezone.now)
    total_sold_litres = models.DecimalField(verbose_name="Total consumed/sold ltrs", max_digits=9, decimal_places=4)
    person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        sales = Sale.objects.all().order_by('-date')

        if not sales:
            self.litres_per_day = self.total_sold_litres
            super().save(*args, **kwargs)
        
        else:
            sale = sales.first()

            day_sales = self.total_sold_litres - sale.total_sold_litres

            self.litres_per_day = day_sales

            super().save(*args, **kwargs)


class DateAbstract(models.Model):
    date = models.DateField(default=date.today)

    class Meta:
        abstract = True


class Price(Common, DateAbstract):

    def __str__(self):
        return str(self.price_per_litre)
    
    class Meta:
        verbose_name_plural = "Fuel price"


class LitresBeforeNextTopUp(models.Model):
    litres = models.DecimalField(max_digits=8, decimal_places=3)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.litres)

    class Meta:
        verbose_name_plural = "Litres before next top up"


class FuelLitre(DateAbstract):
    fuel_litres = models.PositiveSmallIntegerField(verbose_name="Fuel litres (Update fuel litres on every top up.)")

    def __str__(self):
        return f"{self.fuel_litres} litres"

    # def save(self, *args, **kwargs):
        # LitresBeforeNextTopUp.objects.create(litres=self.fuel_litres)
        # super().save(*args, **kwargs)

