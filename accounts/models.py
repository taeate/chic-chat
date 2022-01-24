from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    friends = models.ManyToManyField('self')
    password1 = models.CharField(max_length=50)
    password2 = models.CharField(max_length=50)

