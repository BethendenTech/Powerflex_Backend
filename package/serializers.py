from rest_framework import serializers
from .models import Package, Appliance


class ApplianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appliance
        fields = [
            "id",
            "name",
            "power_w",
            "description",
        ]  # Add fields you want to include


class PackageSerializer(serializers.ModelSerializer):
    appliances = ApplianceSerializer(many=True, read_only=True)  # Nested serializer

    class Meta:
        model = Package
        fields = [
            "id",
            "name",
            "image",
            "price",
            "discount_price",
            "runtime",
            "description",
            "appliances",  # Include the nested serializer
        ]
