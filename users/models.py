from django.db import models

# Create your models here.

class UserDetail(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=511)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email
    

class Quote(models.Model):
    user = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    total_cost_naira = models.FloatField()
    total_cost_usd = models.FloatField()
    number_of_panels = models.IntegerField()
    number_of_inverters = models.IntegerField()
    number_of_batteries = models.IntegerField()
    total_cost_with_profit = models.FloatField()
    total_load_kwh = models.FloatField()
    load_covered_by_solar = models.FloatField()
    total_panel_cost_usd = models.FloatField()
    total_inverter_cost_usd = models.FloatField()
    total_battery_cost_usd = models.FloatField()
    total_panel_cost_naira = models.FloatField()
    total_inverter_cost_naira = models.FloatField()
    total_battery_cost_naira = models.FloatField()
    miscellaneous_cost = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    price_band = models.CharField(max_length=255)
    electricity_spend = models.DecimalField(max_digits=10, decimal_places=2)
