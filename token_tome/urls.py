from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("students/", views.StudentList.as_view(), name="students"),
    path("students/<slug:name>", views.SingleStudent.as_view(), name="single_student"),
    path("users/", views.UserList.as_view(), name="students"),
    path("users/<slug:username>", views.SingleUser.as_view(), name="students"),

]
