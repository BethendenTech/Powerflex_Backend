# users/urls.py
from django.urls import path
from .views import appliance_category_list

urlpatterns = [
    path("categories/", appliance_category_list, name="appliance-category-list"),
]
