from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models

from accounts.managers import CustomUserManager


def validate_min_length(value, min_length):
    if len(value) < min_length:
        raise ValidationError(f'This field must be at least {min_length} characters long.')


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(
        max_length=64, unique=True, verbose_name='email address',
        validators=[MinLengthValidator(limit_value=6)]
    )
    country = models.CharField(
        max_length=64, blank=True, null=False,
        validators=[MinLengthValidator(limit_value=2)]
    )
    city = models.CharField(
        max_length=64, blank=True, null=False,
        validators=[MinLengthValidator(limit_value=2)]
    )
    phone = models.CharField(
        max_length=16, blank=True, null=False,
        validators=[MinLengthValidator(limit_value=9)]
    )
    is_organizer = models.BooleanField(default=False, verbose_name='organizer')
    edited = models.DateTimeField(auto_now=True, blank=True, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
