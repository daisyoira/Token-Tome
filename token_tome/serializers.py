from rest_framework import serializers
from token_tome.models import Student
from django.contrib.auth.models import User


class StudentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Student
        fields = ['url', 'id', 'name', 'token']


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'id', 'username']
