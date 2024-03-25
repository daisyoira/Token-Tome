from django.urls import path

from . import views

urlpatterns = [
    path("", views.api_root, name="index"),
    path("students/", views.StudentList.as_view(), name="student-list"),
    path("students/<slug:pk>", views.StudentDetail.as_view(), name="student-detail"),
    path("students/<slug:name>", views.StudentName.as_view(), name="student-name"),
    path('students/<slug:pk>/highlight/', views.StudentHighlight.as_view(), name="student-highlight"),
    path("users/", views.UserList.as_view(), name="user-list"),
    path("users/<slug:pk>", views.UserDetail.as_view(), name="user-detail"),
    path('users/<slug:pk>/highlight/', views.UserHighlight.as_view(), name="user-highlight")
]
