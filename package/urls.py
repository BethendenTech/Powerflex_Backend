# users/urls.py
from django.urls import path
from .views import package_list, package_detail, package_request

urlpatterns = [
    path("packages/", package_list, name="package-list"),
    path("package-detail/<int:pk>/", package_detail, name="package-detail"),
    path("package-request/", package_request, name="package-request"),
]
