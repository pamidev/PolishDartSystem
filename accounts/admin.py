from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = (
        'email', 'first_name', 'last_name',
        'is_player', 'is_judge', 'is_organizer', 'is_staff', 'is_active',
    )

    list_filter = (
        'is_player', 'is_judge', 'is_organizer', 'is_staff', 'is_active',
    )

    fieldsets = (
        (None, {
            'fields': ('email', 'password',)
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'country', 'city', 'phone',)
        }),
        ('Functions', {
            'fields': [('is_player', 'is_judge', 'is_organizer')]
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser',)
        }),
    )

    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2',)
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'country', 'city', 'phone',)
        }),
        ('Functions', {
            'fields': [('is_player', 'is_judge', 'is_organizer')]
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser',)
        }),
    )

    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('last_name', 'first_name',)


admin.site.register(CustomUser, CustomUserAdmin)
