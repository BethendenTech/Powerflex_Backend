from django.db import models
from product.models import Product

# Create your models here.


class UserDetail(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=511)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email


class Quote(models.Model):
    user = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    quote_number = models.CharField(max_length=255, blank=True, null=True)
    electricity_spend = models.DecimalField(max_digits=10, decimal_places=2)
    price_band = models.CharField(max_length=255)

    additional_info = models.BooleanField(null=True)
    battery_autonomy_days = models.IntegerField(null=True)
    battery_autonomy_hours = models.IntegerField(null=True)
    battery_autonomy_hours_only = models.IntegerField(null=True)
    solar_load = models.FloatField(null=True)

    total_cost_naira = models.FloatField(blank=True, null=True)
    total_cost_usd = models.FloatField(blank=True, null=True)
    number_of_panels = models.IntegerField(blank=True, null=True)
    number_of_inverters = models.IntegerField(blank=True, null=True)
    number_of_batteries = models.IntegerField(blank=True, null=True)
    total_cost_with_profit = models.FloatField(blank=True, null=True)
    total_load_kwh = models.FloatField(blank=True, null=True)
    load_covered_by_solar = models.FloatField(blank=True, null=True)
    total_panel_cost_usd = models.FloatField(blank=True, null=True)
    total_inverter_cost_usd = models.FloatField(blank=True, null=True)
    total_battery_cost_usd = models.FloatField(blank=True, null=True)
    total_panel_cost_naira = models.FloatField(blank=True, null=True)
    total_inverter_cost_naira = models.FloatField(blank=True, null=True)
    total_battery_cost_naira = models.FloatField(blank=True, null=True)
    installer_cost = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class QuoteProduct(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField(null=True)
