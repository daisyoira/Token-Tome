from rest_framework import serializers
from token_tome.models import Student
from django.contrib.auth.models import User


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    highlight = serializers.HyperlinkedIdentityField(view_name='student',
                                                     format='html')

    class Meta:
        model = Student
        fields = ['id', 'username', 'token']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    highlight = serializers.HyperlinkedIdentityField(view_name='user-list',
                                                     format='html',
                                                     read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username']
