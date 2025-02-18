from rest_framework import serializers
from .models import Package, Appliance, PackageProduct, PackageOrder


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


class PackageOrderSerializer(serializers.ModelSerializer):
    package = serializers.PrimaryKeyRelatedField(queryset=Package.objects.all())
    name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    phone_number = serializers.CharField(write_only=True)
    is_finance = serializers.BooleanField(default=False)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = PackageOrder
        fields = [
            "id",
            "package",
            "name",
            "email",
            "phone_number",
            "is_finance",
            "total_price",
        ]

    def create(self, validated_data):
        package = validated_data.pop("package")
        order = PackageOrder.objects.create(package=package, **validated_data)
        order.save()
        return order


class PackageOrderViewSerializer(serializers.ModelSerializer):
    package = PackageSerializer()

    class Meta:
        model = PackageOrder
        fields = [
            "id",
            "package",
            "name",
            "email",
            "phone_number",
            "is_finance",
            "total_price",
        ]
