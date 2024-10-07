# users/serializers.py
from rest_framework import serializers
from .models import UserDetail, Quote
from .utils import calculate_quote

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = ['name', 'email', 'phone_number']

# class QuoteSerializer(serializers.Serializer):
#     electricity_spend = serializers.DecimalField(max_digits=10, decimal_places=2)
#     price_band = serializers.CharField(max_length=255)

#     def create(self, validated_data):
#         calculated_values = calculate_quote(validated_data['electricity_spend'], validated_data['price_band'])
#         Quote.objects.create(**calculated_values)
#         return calculated_values

class QuoteSerializer(serializers.Serializer):
    electricity_spend = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True)
    price_band = serializers.CharField(max_length=255, write_only=True)
    solar_load = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True)
    battery_autonomy_hours = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True)
    breakdowns = serializers.JSONField(write_only=True)
    total_cost_naira = serializers.FloatField(read_only=True)
    total_cost_usd = serializers.FloatField(read_only=True)
    number_of_panels = serializers.IntegerField(read_only=True)
    number_of_inverters = serializers.IntegerField(read_only=True)
    number_of_batteries = serializers.IntegerField(read_only=True)
    total_cost_with_profit = serializers.FloatField(read_only=True)
    total_load_kwh = serializers.FloatField(read_only=True)
    load_covered_by_solar = serializers.FloatField(read_only=True)
    total_panel_cost_usd = serializers.FloatField(read_only=True)
    total_inverter_cost_usd = serializers.FloatField(read_only=True)
    total_battery_cost_usd = serializers.FloatField(read_only=True)
    total_panel_cost_naira = serializers.FloatField(read_only=True)
    total_inverter_cost_naira = serializers.FloatField(read_only=True)
    total_battery_cost_naira = serializers.FloatField(read_only=True)
    miscellaneous_cost = serializers.FloatField(read_only=True)

    def create(self, validated_data):
        calculated_values = calculate_quote(validated_data['electricity_spend'], validated_data['price_band'], validated_data['solar_load'], validated_data['battery_autonomy_hours'], validated_data['breakdowns'])
        Quote.objects.create(**calculated_values)
        return calculated_values