from django.db import models
from product.models import Product, Appliance

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

    is_finance = models.BooleanField(null=True)

    installation_and_cabling = models.FloatField(blank=True, null=True)
    installer_commission = models.FloatField(blank=True, null=True)
    installer_commission_amount = models.FloatField(blank=True, null=True)
    load_covered_by_solar = models.FloatField(blank=True, null=True)
    total_cost_naira = models.FloatField(blank=True, null=True)
    total_cost_usd = models.FloatField(blank=True, null=True)
    total_cost_with_profit = models.FloatField(blank=True, null=True)
    total_equipments = models.FloatField(blank=True, null=True)
    total_load_kwh = models.FloatField(blank=True, null=True)
    total_vat = models.FloatField(blank=True, null=True)
    vat = models.FloatField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)


class QuoteAppliance(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    appliance = models.ForeignKey(Appliance, on_delete=models.CASCADE)
    quantity = models.FloatField(null=True)
    usage = models.FloatField(null=True)


class QuoteProduct(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField(null=True)
