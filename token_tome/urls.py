from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("users/", views.user_list, name="users"),
    path("users/<slug:username>", views.single_user, name="index")

]