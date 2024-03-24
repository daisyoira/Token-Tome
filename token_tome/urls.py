from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("users/", views.UserList.as_view(), name="users"),
    path("users/<slug:username>", views.SingleUser.as_view(), name="single_user")

]