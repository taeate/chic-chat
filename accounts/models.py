from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    friends = models.ManyToManyField('self')
    password1 = models.CharField(max_length=50)
    password2 = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50, unique=True)
    email = False
