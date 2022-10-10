from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    """User Model Definition"""

    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)
    name = models.CharField(max_length=150, verbose_name="이름")

    def __str__(self):
        return self.name
