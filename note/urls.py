from django.urls import path
from . import views

urlpatterns = [
    path("new/", views.create_note, name="create_note"),
    path("show/<str:url_key>", views.show_note,name="show_note"),
    path("home/",views.home, name="home")
]
