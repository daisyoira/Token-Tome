from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.FileUploadFormView.as_view()),
    path("create-student", views.StudentCreateView.as_view()),
    re_path("download/(?P<file_name>[-a-zA-Z0-9_]+)\\Z", views.FileDownloadView.as_view(), name='download'),
    path("student-token/<int:pk>", views.StudentDetailView.as_view(), name='student-token'),
    path("api", views.api_root, name="index"),
    path("api/students/", views.StudentList.as_view(), name="student-list"),
    path("api/students/<slug:pk>", views.StudentDetail.as_view(), name="student-detail"),
    path("api/students/<slug:name>", views.StudentName.as_view(), name="student-name"),
    path('api/students/<slug:pk>/highlight/', views.StudentHighlight.as_view(), name="student-highlight"),
    path("api/users/", views.UserList.as_view(), name="user-list"),
    path("api/users/<slug:pk>", views.UserDetail.as_view(), name="user-detail"),
    path('api/users/<slug:pk>/highlight/', views.UserHighlight.as_view(), name="user-highlight"),
    path('api/upload/', views.FileUploadView.as_view(), name='file_upload')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

