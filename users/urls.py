# users/urls.py
from django.urls import path
from .views import submit_user_details, calculate_quote

urlpatterns = [
    path('submit-details/', submit_user_details, name='submit_details'),
    path('calculate-quote/', calculate_quote, name='calculate_quote'),
]
