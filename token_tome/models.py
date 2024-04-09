import secrets

from django.db import models
# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=200)
    token = models.CharField(max_length=100,
                             unique=True,
                             editable=False,
                             default=secrets.token_urlsafe(7))
