from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'email',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'country',
            'city',
            'phone',
        ]


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = [
            'email',
            'password',
            'first_name',
            'last_name',
            'country',
            'city',
            'phone',
        ]


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]
