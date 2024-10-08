from django.urls import path
from . import views

urlpatterns = [
    path("new/", views.create_note),
    path("show/<str:url>", views.show_note),
]
