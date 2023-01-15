from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


# class MyUserManager(BaseUserManager):
#     def create_user(self, email, username, password=None):
#         if not email:
#             raise ValueError('Users must have an email address')
#
#         user = self.model(
#             email=self.normalize_email(email),
#             username=username
#         )
#
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, username, password=None):
#         """
#         Creates and saves a superuser with the given email, date of
#         birth and password.
#         """
#         user = self.create_user(
#             username=username,
#             email='admin@admin.com',
#             password=password,
#         )
#         user.is_admin = True
#         user.is_active = True
#         user.save(using=self._db)
#         return user


# class CustomUser(AbstractBaseUser):
#     email = models.EmailField(
#         verbose_name='email address',
#         max_length=255,
#         unique=True,
#     )
#     username = models.CharField(verbose_name='username', unique=True, max_length=30)
#     is_active = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#
#     objects = MyUserManager()
#
#     USERNAME_FIELD = 'username'
#
#     def __str__(self):
#         return self.get_username()
#
#     def has_perm(self, perm, obj=None):
#         return True
#
#     def has_module_perms(self, app_label):
#         return True
#
#     @property
#     def is_staff(self):
#         "Is the user a member of staff?"
#         # Simplest possible answer: All admins are staff
#         return self.is_admin
#

class CustomUser(AbstractUser):
    pass


    def __str__(self):
        return self.username
