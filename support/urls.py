# users/urls.py
from django.urls import path
from .views import create_contact

urlpatterns = [
    path("create-contact/", create_contact, name="create-contact"),
]
