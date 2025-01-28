from rest_framework import serializers
from .models import Appliance, ApplianceCategory, Band


class ApplianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appliance
        fields = ["id", "name", "power_w", "description"]


class ApplianceCategorySerializer(serializers.ModelSerializer):
    appliances = ApplianceSerializer(many=True, read_only=True)

    class Meta:
        model = ApplianceCategory
        fields = ["id", "name", "type", "appliances"]


class BandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Band
        fields = ["id", "name", "hours_supply", "price", "description"]
