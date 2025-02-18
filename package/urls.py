# users/urls.py
from django.urls import path
from .views import (
    package_list,
    package_detail,
    package_request,
    package_order,
    package_order_detail,
)

urlpatterns = [
    path("packages/", package_list, name="package-list"),
    path("package-detail/<int:pk>/", package_detail, name="package-detail"),
    path("package-request/", package_request, name="package-request"),
    path("package-order/", package_order, name="package-order"),
    path("package-order-detail/<int:pk>/", package_order_detail, name="package-order-detail"),
]
