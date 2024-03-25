from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from rest_framework import status
from rest_framework import generics
from rest_framework import permissions, renderers
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from token_tome.models import Student
from django.contrib.auth.models import User
from token_tome.serializers import StudentSerializer, UserSerializer
# Create your views here.


def index(request):
    return HttpResponse("Hello, world!")


@api_view
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'students': reverse('student-list', request=request, format=format)
    })


class StudentHighlight(generics.GenericAPIView):
    queryset = Student.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


#@csrf_exempt
#@api_view
class StudentList(APIView):
    """
    List all users, or create a new user.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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


#@csrf_exempt
#@api_view
class SingleStudent(APIView):
    """
    Retrieve, update or delete a user's information.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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


class SingleUser(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
