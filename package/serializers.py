from rest_framework import serializers
from .models import (
    Package,
    Appliance,
    PackageProduct,
    PackageOrder,
    PackageOrderApplication,
)


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


class PackageOrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageOrder
        fields = [
            "id",
            "name",
            "email",
            "phone_number",
            "is_finance",
            "total_price",
            "status",
        ]

    def update(self, instance, validated_data):
        # Update all fields provided in the validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PackageApplicationSerializer(serializers.ModelSerializer):
    packageOrder = serializers.PrimaryKeyRelatedField(queryset=PackageOrder.objects.all())
    application_type = serializers.CharField(write_only=True)
    bvn = serializers.CharField(write_only=True)
    other_role = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    house_number = serializers.CharField(write_only=True)
    street_address = serializers.CharField(write_only=True)
    landmark = serializers.CharField(write_only=True)
    bus_stop = serializers.CharField(write_only=True)
    occupation = serializers.CharField(write_only=True)
    business_role = serializers.CharField(write_only=True)
    business_name = serializers.CharField(write_only=True)
    business_address = serializers.CharField(write_only=True)
    town = serializers.CharField(write_only=True)
    city = serializers.CharField(write_only=True)
    state = serializers.CharField(write_only=True)
    lga = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    phone_number = serializers.CharField(write_only=True)
    reference_phone1 = serializers.CharField(write_only=True)
    reference_phone2 = serializers.CharField(write_only=True)
    how_heard_about = serializers.CharField(write_only=True)
    applicant_id_card = serializers.CharField(required=False, allow_null=True)
    company_registration_document = serializers.CharField(
        required=False, allow_null=True
    )
    bank_statements = serializers.CharField(required=False, allow_null=True)
    recent_utility_bill = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = PackageOrderApplication
        fields = [
            "id",
            "packageOrder",
            "application_type",
            "bvn",
            "other_role",
            "first_name",
            "last_name",
            "house_number",
            "street_address",
            "landmark",
            "bus_stop",
            "occupation",
            "business_role",
            "business_name",
            "business_address",
            "town",
            "city",
            "state",
            "lga",
            "email",
            "phone_number",
            "reference_phone1",
            "reference_phone2",
            "how_heard_about",
            "applicant_id_card",
            "company_registration_document",
            "bank_statements",
            "recent_utility_bill",
        ]

    def create(self, validated_data):
        packageOrder = validated_data.pop("packageOrder")
        application = PackageOrderApplication.objects.create(
            packageOrder=packageOrder, **validated_data
        )
        application.save()
        return application
