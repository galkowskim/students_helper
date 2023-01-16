from django.contrib.auth.models import (
    AbstractBaseUser
)
from django.contrib.auth.models import User, AbstractUser


class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username
