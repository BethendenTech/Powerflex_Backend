from rest_framework import serializers
from .models import Package


class PackageSerializer(serializers.ModelSerializer):
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
            "appliances",
        ]
