from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, phone,fullname):
        if not email:
            raise ValueError(_('Почта обязательно'))
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone,fullname=fullname)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
  
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):

    phone = models.CharField(max_length=255,null=True)
    fullname = models.CharField(max_length=255,null=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    username = models.CharField(max_length=255)

    REQUIRED_FIELDS = ()
    objects = CustomUserManager()

    def __str__(self):
        return self.email
