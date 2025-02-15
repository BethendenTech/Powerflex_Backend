from rest_framework import serializers
from .models import Package, Appliance, PackageProduct


class ApplianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appliance
        fields = [
            "id",
            "name",
            "power_w",
            "description",
        ]  # Add fields you want to include


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageProduct
        fields = [
            "id",
            "name",
            "price",
            "quantity",
        ]  # Add fields you want to include


class PackageSerializer(serializers.ModelSerializer):
    appliances = ApplianceSerializer(many=True, read_only=True)  # Nested serializer
    products = (
        serializers.SerializerMethodField()
    )  # Use SerializerMethodField to fetch related products

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
            "products",  # Include the nested serializer
        ]

    def get_products(self, obj):
        # Fetch related PackageProduct instances using the reverse relationship
        products = obj.package_products.all()
        return ProductSerializer(products, many=True).data
