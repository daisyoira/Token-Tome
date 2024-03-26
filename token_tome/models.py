from django.db import models
# Create your models here.


# field: blank=True, the field is allowed
# to be blank; default is False
class Student(models.Model):
    name = models.CharField(max_length=200)
    token = models.CharField(max_length=100,
                             unique=True,
                             editable=False)
