from django.db import models
# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=200)
    token = models.CharField(max_length=100)
