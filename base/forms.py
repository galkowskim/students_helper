from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser


class CustomUserChangeForm(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get("password")
        if password:
            password.help_text = 'Raw passwords are not stored, so there is no way to see this user’s password, ' \
                                 'but you can change the password using <a href="../change_password/">this form</a>.'
    class Meta:
        model = CustomUser
        fields = ("username", "email")


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='A valid email address, please.', required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        if CustomUser.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("The given email is already registered")
        return self.cleaned_data['email']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
