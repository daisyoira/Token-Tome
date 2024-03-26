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

from rest_framework import filters
# Create your views here.


def index(request):
    return HttpResponse("Hello, world!")


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'students': reverse('student-list', request=request, format=format)
    })


class StudentHighlight(generics.GenericAPIView):
    queryset = Student.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        student = self.get_object()
        return Response(student.highlighted)


#@csrf_exempt
#@api_view
class StudentList(generics.ListCreateAPIView):
    """
    List all users, or create a new user.
    """
    permission_classes = [permissions.IsAuthenticated]
    name = 'student-list'

    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'token']


#@csrf_exempt
#@api_view
class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a user's information.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    name = 'student-detail'

    # check if the user exists
    '''def try_get(self, name):
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
'''


class StudentName(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a user's information.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = Student.name
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    name = 'student-name'


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    name = 'user-list'


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    name = 'user-detail'


class UserHighlight(generics.GenericAPIView):
    queryset = Student.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]
    name = 'user-highlight'

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        return Response(user.highlighted)
