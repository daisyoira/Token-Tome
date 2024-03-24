from django.test import TestCase

# Create your tests here.
from token_tome.models import User
from token_tome.serializers import UserSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


#snippet = User(username='test_1', token='121ew')
snippet = User(username='test_1')
# saves to db
snippet.save()

serializer = UserSerializer(snippet)
print(serializer.data)

content = JSONRenderer().render(serializer.data)
print(content)
content = JSONRenderer().render(serializer.data)
content

import io

stream = io.BytesIO(content)
data = JSONParser().parse(stream)
serializer = UserSerializer(data=data)
serializer.is_valid()

serializer.validated_data
serializer.save()
