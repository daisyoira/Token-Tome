from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, FormView
from django.conf import settings

from rest_framework import status
from rest_framework import generics
from rest_framework import permissions, renderers
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.parsers import MultiPartParser

from token_tome.models import Student, File
from token_tome.forms import FileUploadForm
from django.contrib.auth.models import User
from token_tome.serializers import StudentSerializer, UserSerializer, FileUploadSerializer
from token_tome.forms import FileUploadForm

from io import BytesIO, StringIO
from fpdf import FPDF
from pypdf import PdfWriter, PdfReader, Transformation
import os

from rest_framework import filters
# Create your views here.


def index(request):
    return HttpResponse("Hello, world!")


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'students': reverse('student-list', request=request, format=format),
        'upload': reverse('file_upload', request=request, format=format)
    })


class StudentCreateView(CreateView):
    model = Student
    fields = ['name']

    # get primary key and redirect to individual student
    # page
    def get_success_url(self):
        return reverse('student-token', kwargs={'pk': self.object.pk})


class StudentDetailView(DetailView):
    model = Student
    fields = '__all__'
    context_object_name = 'student'


class FileUploadFormView(FormView):
    form_class = FileUploadForm
    template_name = 'token_tome/file_form.html'
    success_url = 'create-student'


class StudentHighlight(generics.GenericAPIView):
    queryset = Student.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        student = self.get_object()
        return Response(student.highlighted)


# Source: https://backendengineer.io/django-rest-framework-file-upload-api/
class FileUploadView(generics.CreateAPIView):
    parser_classes = [MultiPartParser]
    serializer_class = FileUploadSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            uploaded_file = serializer.validated_data["file_path"]

            watermark_pdf = FPDF()
            watermark_pdf.set_font('Helvetica', 'B', 20)
            watermark_pdf.add_page()

            # add token to pdf to be used as watermark
            # set opacity to 0, so it's invisible
            with watermark_pdf.local_context(fill_opacity=0.25):
                watermark_pdf.text(x=50, y=50, text=serializer.validated_data["student"])

            with watermark_pdf.local_context(fill_opacity=0):
                watermark_pdf.text(x=100, y=50, text=serializer.validated_data["student"])
            #save_watermark = BytesIO()
            #save_to_folder = watermark_pdf.output(name=os.path.join(settings.MEDIA_ROOT,

            # save the pdf to be used for watermarking as
            # a bytestring in memory
            watermark_byte_string = watermark_pdf.output(dest='S')
            saved_watermark = BytesIO(watermark_byte_string)

            # get the first page of the pdf to be used
            # as a watermark
            stamp = PdfReader(saved_watermark).pages[0]

            # write to the uploaded pdf
            writer = PdfWriter(clone_from=serializer.validated_data["file_path"])
            #reader = PdfReader(serializer.validated_data["file_path"])

            #writer.append(reader, pages=reader.page)

            # loop through the pages in the uploaded pdf
            # and add the watermark to every page
            for page in writer.pages:
                page.merge_page(stamp, over=True)

            # save the watermarked pdf to the media directory
            # in the project
            path = os.path.join(settings.MEDIA_ROOT,
                                'watermark_'+serializer.validated_data["file_path"].name)
            writer.write(path)

            data = {
                "file_path": path,
                "student": serializer.validated_data["student"]
            }

            return Response(data=data,
                            status=204)

        return Response(data=serializer.errors,
                        status=400)


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
