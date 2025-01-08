# users/urls.py
from django.urls import path
from .views import (
    submit_user_details,
    calculate_quote,
    create_quote,
    create_quote_application,
    calculate_financing,
    create_quote_step_1,
    create_quote_step_2,
    create_quote_step_3,
    payment_quote,
    upload_file,
    mail_quote,
)

urlpatterns = [
    path("submit-details/", submit_user_details, name="submit_details"),
    path("mail-quote/", mail_quote, name="mail_quote"),
    path("calculate-quote/", calculate_quote, name="calculate_quote"),
    path("calculate-financing/", calculate_financing, name="calculate_financing"),
    path("create-quote/", create_quote, name="create_quote"),
    path("payment-quote/", payment_quote, name="payment_quote"),
    path(
        "cerate-quote-application/",
        create_quote_application,
        name="create_quote_application",
    ),
    path("create-quote-step-1/", create_quote_step_1, name="create_quote_step_1"),
    path("create-quote-step-2/", create_quote_step_2, name="create_quote_step_1"),
    path("create-quote-step-3/", create_quote_step_3, name="create_quote_step_1"),
    path("upload-file/", upload_file, name="upload_file"),
]
