from django.shortcuts import render

# Create your views here.

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserDetail
from .serializers import (
    UserDetailSerializer,
    QuoteSerializer,
    FinanceSerializer,
    CreateQuoteSerializer,
    CreateQuoteStep1Serializer,
)
from .utils import generate_quote_number


@api_view(["POST"])
def submit_user_details(request):
    serializer = UserDetailSerializer(data=request.data)
    if serializer.is_valid():
        # If data is valid, attempt to create the user
        user, created = UserDetail.objects.get_or_create(
            email=serializer.validated_data["email"],
            defaults=serializer.validated_data,
        )

        response_data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone_number": user.phone_number,
        }

        if created:
            return Response(
                {
                    "message": "User created successfully.",
                    "user": response_data,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                    "message": "User already exists.",
                    "user": response_data,
                },
                status=status.HTTP_200_OK,
            )
    else:
        # Check if the email is the issue and return the existing user
        email = request.data.get("email")
        if email:
            try:
                user = UserDetail.objects.get(email=email)
                response_data = {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "phone_number": user.phone_number,
                }
                return Response(
                    {
                        "message": "User already exists.",
                        "user": response_data,
                    },
                    status=status.HTTP_200_OK,
                )
            except UserDetail.DoesNotExist:
                pass
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def calculate_quote(request):
    if request.method == "POST":
        serializer = QuoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def calculate_financing(request):
    if request.method == "POST":
        serializer = FinanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_quote(request):
    if request.method == "POST":
        serializer = CreateQuoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_quote_step_1(request):
    if request.method == "POST":
        user_id = request.data.get("user_id")
        if not user_id:
            return Response(
                {"error": "user_id is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Fetch the user
        try:
            user = UserDetail.objects.get(id=user_id)
        except UserDetail.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Initialize the serializer with the data and context (user)
        serializer = CreateQuoteStep1Serializer(
            data=request.data, context={"user": user}
        )

        # Check if the data is valid
        if serializer.is_valid():
            # Save the quote object
            quote = serializer.save()

            response_data = {"quote_number": quote.quote_number}

            print("response_data", response_data)
            # Return the serialized quote data in the response
            return Response(
                {
                    "message": "Quote created successfully.",
                    "quote": response_data,  # Return serialized quote data
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
