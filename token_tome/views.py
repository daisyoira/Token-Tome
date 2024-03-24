from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from token_tome.models import Student
from django.contrib.auth.models import User
from token_tome.serializers import StudentSerializer, UserSerializer
# Create your views here.


def index(request):
    return HttpResponse("Hello, world!")


@csrf_exempt
@api_view
class StudentList(APIView):
    """
    List all users, or create a new user.
    """
    def get(self, request):
        users = Student.objects.all()
        serializer = StudentSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,
                                status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view
class SingleStudent(APIView):
    """
    Retrieve, update or delete a user's information.
    """
    # check if the user exists
    def try_get(self, name):
        try:
            self.student = Student.objects.get(name=name)
        except Student.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        serializer = StudentSerializer(self.student)
        return JsonResponse(serializer.data)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = StudentSerializer(data=data)

        # check if all the fields have been filled
        # before saving to the database
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
