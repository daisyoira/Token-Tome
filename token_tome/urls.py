from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.FileUploadFormView.as_view()),
    path("create-student", views.StudentCreateView.as_view()),
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
]
