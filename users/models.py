from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField

class CustomAccountManager(BaseUserManager):
    def create_user(self, username, email, contact, password, **other_fields):
        if not username:
            raise ValueError("Username must be provided/required")

        email = self.normalize_email(email)

        user = self.model(username=username, email=email, contact=contact, **other_fields)

        user.set_password(password)

        user.save()

        return user

    
    def create_superuser(self, username, email, contact, password, **other_fields):
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_superuser') is not True:
            raise ValueError("For superuser, 'is_superuser' value must be True")
        
        if other_fields.get('is_staff') is not True:
            raise ValueError("For superuser, 'is_staff' value is to be True")

        
        return self.create_user(username, email, contact, password, **other_fields)



class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=60, unique=True)
    contact = PhoneNumberField()
    date_joined = models.DateTimeField(default=timezone.now)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email', 'contact']


