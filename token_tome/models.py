import secrets

from django.db import models
# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=200,
                            null=False)
    token = models.CharField(max_length=100,
                             unique=True,
                             editable=False,
                             default=secrets.token_urlsafe(7))
    institution = models.CharField(max_length=200,
                                   null=False,
                                   default='Curtin')

    def save(self, *args, **kwargs):
        self.token = secrets.token_urlsafe(7)
        super(Student, self).save(*args, **kwargs)

    class Meta:
        managed = True


def choices():
    token_choices = []
    try:
        token_choices = [(student.token, student.name) for student in Student.objects.all()]
    except Exception as err:
        token_choices = []
    return token_choices
    pass

class File(models.Model):

    ''''TOKEN_CHOICES = []
    try:
        TOKEN_CHOICES = [(student.token, student.name) for student in Student.objects.all()]
    except Exception as err:
        TOKEN_CHOICES = []'''''

    file = models.FileField()
    #student  = models.ForeignKey(Student,
    #                             on_delete=models.CASCADE,
    #                             )
    student = models.CharField(max_length=100,
                               choices=choices(),
                               )

    #def __init__(self):
    #    super(File, self).__init__()
        #self._meta.get_field('student').choices = choices()


    # stop creation of table in database
    class Meta:
        managed = False
        db_table = 'file'

