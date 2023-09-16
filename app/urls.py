from django.urls import path
from .views import home, expenses

urlpatterns = [
    path('', home, name="home"),
    path('expenses/', expenses, name="expenses")
]
