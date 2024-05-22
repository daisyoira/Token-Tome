from rest_framework import serializers
from token_tome.models import Student, File
from django.contrib.auth.models import User


class StudentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Student
        fields = ['url', 'id', 'name', 'token', 'institution']


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'id', 'username']


class FileUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = '__all__'
