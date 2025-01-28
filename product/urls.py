# users/urls.py
from django.urls import path
from .views import appliance_category_list, band_list

urlpatterns = [
    path("categories/", appliance_category_list, name="appliance-category-list"),
    path("bands/", band_list, name="band-list"),
]