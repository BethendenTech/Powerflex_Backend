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
)


@api_view(["POST"])
def submit_user_details(request):
    if request.method == "POST":
        serializer = UserDetailSerializer(data=request.data)
        if serializer.is_valid():
            # Assuming the unique user detail is 'email' or 'username'
            email = serializer.validated_data.get("email")  # or 'username'

            # Use get_or_create to either fetch the user or create a new one
            user, created = UserDetail.objects.get_or_create(
                email=email, defaults=serializer.validated_data
            )

            if created:
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )  # User created
            else:
                return Response(
                    {"detail": "User already exists"}, status=status.HTTP_200_OK
                )  # User already exists

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
