from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    friends = models.ManyToManyField('self')
    nickname = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=False)
    email = False
