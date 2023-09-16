from django.contrib import admin
from .models import Price, Sale, FuelLitre, LitresBeforeNextTopUp, Expense

admin.site.register(Sale)
admin.site.register(Price)
admin.site.register(FuelLitre)
admin.site.register(LitresBeforeNextTopUp)
admin.site.register(Expense)
