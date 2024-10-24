# users/urls.py
from django.contrib import admin
from django.urls import path
from .views import submit_user_details, calculate_quote, create_quote

urlpatterns = [
    path('admin/', admin.site.urls),
    path('submit-details/', submit_user_details, name='submit_details'),
    path('calculate-quote/', calculate_quote, name='calculate_quote'),
    path('create-quote/', create_quote, name='create_quote'),
]
