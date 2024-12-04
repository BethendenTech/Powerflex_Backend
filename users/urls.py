# users/urls.py
from django.urls import path
from .views import (
    submit_user_details,
    calculate_quote,
    create_quote,
    calculate_financing,
    create_quote_step_1,
)

urlpatterns = [
    path("submit-details/", submit_user_details, name="submit_details"),
    path("calculate-quote/", calculate_quote, name="calculate_quote"),
    path("calculate-financing/", calculate_financing, name="calculate_financing"),
    path("create-quote/", create_quote, name="create_quote"),
    path("create-quote-step-1/", create_quote_step_1, name="create_quote_step_1"),
]
