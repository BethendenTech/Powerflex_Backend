# users/urls.py
from django.urls import path
from .views import package_list, package_detail

urlpatterns = [
    path("packages/", package_list, name="package-list"),
    path("packages/<int:pk>/", package_detail, name="package-detail"),
]
