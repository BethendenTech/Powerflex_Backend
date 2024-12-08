# users/serializers.py
from rest_framework import serializers
from .models import UserDetail, Quote, QuoteAppliance
from product.models import Appliance
from .utils import calculate_quote, calculate_financing, generate_quote_number


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = ["name", "email", "phone_number"]

    def validate_email(self, value):
        return value


# class QuoteSerializer(serializers.Serializer):
#     electricity_spend = serializers.DecimalField(max_digits=10, decimal_places=2)
#     price_band = serializers.CharField(max_length=255)

#     def create(self, validated_data):
#         calculated_values = calculate_quote(validated_data['electricity_spend'], validated_data['price_band'])
#         Quote.objects.create(**calculated_values)
#         return calculated_values


class QuoteSerializer(serializers.Serializer):
    electricity_spend = serializers.DecimalField(
        max_digits=10, decimal_places=2, write_only=True
    )
    price_band = serializers.CharField(max_length=255, write_only=True)
    solar_load = serializers.DecimalField(
        max_digits=10, decimal_places=2, write_only=True
    )
    battery_autonomy_hours = serializers.DecimalField(
        max_digits=10, decimal_places=2, write_only=True
    )
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
    installation_and_cabling = serializers.FloatField(read_only=True)
    vat = serializers.FloatField(read_only=True)
    installer_commission = serializers.FloatField(read_only=True)
    installer_commission_amount = serializers.FloatField(read_only=True)
    total_equipments = serializers.FloatField(read_only=True)
    total_vat = serializers.FloatField(read_only=True)
    savings_and_roi = serializers.JSONField(read_only=True)
    products = serializers.JSONField(read_only=True)
    is_finance = serializers.BooleanField(write_only=True)

    def create(self, validated_data):
        calculated_values = calculate_quote(
            validated_data["electricity_spend"],
            validated_data["price_band"],
            validated_data["solar_load"],
            validated_data["battery_autonomy_hours"],
            validated_data["breakdowns"],
            validated_data["is_finance"],
        )
        return calculated_values


class FinanceSerializer(serializers.Serializer):
    total_cost_naira = serializers.FloatField(write_only=True)

    def create(self, validated_data):
        calculated_data = calculate_financing(validated_data["total_cost_naira"])
        return calculated_data


class CreateQuoteSerializer(serializers.Serializer):
    quote_number = serializers.CharField(write_only=True)

    def create(self, validated_data):
        quote_number = validated_data["quote_number"]

        # Retrieve the specific quote instance
        try:
            quote = Quote.objects.get(quote_number=quote_number)
        except Quote.DoesNotExist:
            raise serializers.ValidationError({"error": "Quote not found"})

        # Retrieve the related QuoteAppliance objects
        breakdowns = QuoteAppliance.objects.filter(quote=quote)

        # Ensure breakdowns is in the format calculate_quote expects
        breakdown_list = [
            {
                "appliance_id": appliance.appliance.id,
                "quantity": appliance.quantity,
                "usage": appliance.usage,
            }
            for appliance in breakdowns
        ]

        calculated_values = calculate_quote(
            quote.electricity_spend,
            quote.price_band,
            quote.solar_load,
            quote.battery_autonomy_hours,
            breakdown_list,
        )

        # Set the calculated values to the quote instance
        quote.total_load_kwh = calculated_values.get("total_load_kwh", 0)
        quote.total_cost_naira = calculated_values.get("total_cost_naira", 0)
        quote.total_cost_usd = calculated_values.get("total_cost_usd", 0)

        # Save the updated quote instance
        quote.save()

        return quote


class CreateQuoteStep1Serializer(serializers.Serializer):
    electricity_spend = serializers.DecimalField(
        max_digits=10, decimal_places=2, write_only=True
    )
    price_band = serializers.CharField(max_length=255, write_only=True)

    def create(self, validated_data):
        user = self.context["user"]
        quote_number = validated_data.get(
            "quote_number", generate_quote_number()
        )  # Generate quote_number if not provided
        quote = Quote.objects.create(
            user=user, quote_number=quote_number, **validated_data
        )
        return quote


class CreateQuoteStep2Serializer(serializers.Serializer):
    additional_info = serializers.BooleanField(required=False, allow_null=True)
    battery_autonomy_days = serializers.IntegerField(required=False, allow_null=True)
    battery_autonomy_hours = serializers.IntegerField(required=False, allow_null=True)
    battery_autonomy_hours_only = serializers.IntegerField(
        required=False, allow_null=True
    )
    solar_load = serializers.FloatField(required=False, allow_null=True)

    def create(self, validated_data):
        quote_number = self.context["quote_number"]

        # Retrieve the specific quote instance
        try:
            quote = Quote.objects.get(quote_number=quote_number)
        except Quote.DoesNotExist:
            raise serializers.ValidationError({"error": "Quote not found"})

        # Update fields
        for attr, value in validated_data.items():
            setattr(quote, attr, value)
        quote.save()  # Save the updated instance

        return quote


class CreateQuoteStep3Serializer(serializers.Serializer):
    breakdowns = serializers.JSONField(write_only=True)

    def create(self, validated_data):
        quote_number = self.context["quote_number"]

        # Retrieve the specific quote instance
        try:
            quote = Quote.objects.get(quote_number=quote_number)
        except Quote.DoesNotExist:
            raise serializers.ValidationError({"error": "Quote not found"})

        # Update breakdowns (handling QuoteAppliance)
        breakdowns = validated_data.get("breakdowns", [])
        self.update_quote_appliances(quote, breakdowns)

        return quote

    def update_quote_appliances(self, quote, breakdowns):
        """
        Updates the QuoteAppliance instances associated with a quote.
        """
        # Clear existing appliances for this quote
        QuoteAppliance.objects.filter(quote=quote).delete()

        # Add updated appliances
        for value in breakdowns:
            appliance_id = value.get("appliance_id")
            usage = value.get("usage")
            quantity = value.get("quantity")

            if not appliance_id:
                raise serializers.ValidationError(
                    {"error": "appliance_id is required in breakdowns"}
                )

            # Retrieve the appliance instance
            try:
                appliance = Appliance.objects.get(id=appliance_id)
            except Appliance.DoesNotExist:
                raise serializers.ValidationError(
                    {"error": f"Appliance with ID {appliance_id} not found"}
                )

            # Create or update the QuoteAppliance instance
            QuoteAppliance.objects.create(
                quote=quote, appliance=appliance, quantity=quantity, usage=usage
            )
