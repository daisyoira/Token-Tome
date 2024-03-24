from rest_framework import serializers
from token_tome.models import User


class UserSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'token']