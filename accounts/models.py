from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=128, unique=True, verbose_name='email address')
    country = models.CharField(max_length=128, blank=True, null=False)
    city = models.CharField(max_length=128, blank=True, null=False)
    phone = models.CharField(max_length=16, blank=True, null=False)
    is_player = models.BooleanField(default=True, verbose_name='player')
    is_judge = models.BooleanField(default=False, verbose_name='judge')
    is_organizer = models.BooleanField(default=False, verbose_name='organizer')
    edited = models.DateTimeField(auto_now=True, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
