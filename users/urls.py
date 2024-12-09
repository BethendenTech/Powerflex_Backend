# users/urls.py
from django.urls import path
from .views import (
    submit_user_details,
    calculate_quote,
    create_quote,
    apply_business,
    apply_individual,
    calculate_financing,
    create_quote_step_1,
    create_quote_step_2,
    create_quote_step_3,
)

urlpatterns = [
    path("submit-details/", submit_user_details, name="submit_details"),
    path("calculate-quote/", calculate_quote, name="calculate_quote"),
    path("calculate-financing/", calculate_financing, name="calculate_financing"),
    path("create-quote/", create_quote, name="create_quote"),
    path("apply-business/", apply_business, name="apply_business"),
    path("apply-individual/", apply_individual, name="apply_individual"),
    path("create-quote-step-1/", create_quote_step_1, name="create_quote_step_1"),
    path("create-quote-step-2/", create_quote_step_2, name="create_quote_step_1"),
    path("create-quote-step-3/", create_quote_step_3, name="create_quote_step_1"),
]
