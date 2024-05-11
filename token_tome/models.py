import secrets

from django.db import models
# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=200)
    token = models.CharField(max_length=100,
                             unique=True,
                             editable=False,
                             default=secrets.token_urlsafe(7))

    def save(self, *args, **kwargs):
        self.token = secrets.token_urlsafe(7)
        super(Student, self).save(*args, **kwargs)

    class Meta:
        managed = True


class File(models.Model):

    TOKEN_CHOICES = []
    try:
        TOKEN_CHOICES = [(student.token, student.name) for student in Student.objects.all()]
    except Exception as err:
        TOKEN_CHOICES = []

    file = models.FileField()
    student = models.CharField(max_length=100,
                               choices=TOKEN_CHOICES,
                               )

    # stop creation of table in database
    class Meta:
        managed = False
        db_table = 'file'

