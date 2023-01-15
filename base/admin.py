from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserRegistrationForm, CustomUserChangeForm

from base.models import CustomUser
from django.contrib.auth.models import Group


class CustomUserAdmin(UserAdmin):
    add_form = UserRegistrationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username", ]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)
