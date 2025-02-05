from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=100)
    unique_code = models.CharField(blank=True, null=True)
    model_name = models.CharField(blank=True, null=True)
    model_year = models.CharField(blank=True, null=True)
    country_of_origin = models.CharField(blank=True, null=True)
    capacity_w = models.FloatField(blank=True, null=True)
    capacity_ah = models.FloatField(blank=True, null=True)
    price_usd = models.FloatField(blank=True, null=True)
    voc_v = models.CharField(blank=True, null=True)
    isc_a = models.CharField(blank=True, null=True)
    efficiency = models.FloatField(blank=True, null=True)
    phase_type = models.CharField(blank=True, null=True)
    warranty_years = models.CharField(blank=True, null=True)
    voltage = models.FloatField(blank=True, null=True)
    dod = models.FloatField(blank=True, null=True)
    cycle_life = models.CharField(blank=True, null=True)
    supplier = models.CharField(blank=True, null=True)

    def __str__(self):
        return self.name


class ApplianceCategory(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Appliance(models.Model):
    category = models.ForeignKey(
        ApplianceCategory, on_delete=models.CASCADE, related_name="appliances"
    )
    name = models.CharField(max_length=100)
    power_w = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Band(models.Model):
    name = models.CharField(max_length=100)
    hours_supply = models.FloatField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    tariff = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
