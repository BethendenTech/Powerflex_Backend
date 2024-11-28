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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=100)
    unique_code = models.TextField(blank=True, null=True)
    model_name = models.TextField(blank=True, null=True)
    model_year = models.TextField(blank=True, null=True)
    country_of_origin = models.TextField(blank=True, null=True)
    capacity_w = models.TextField(blank=True, null=True)
    price_usd = models.TextField(blank=True, null=True)
    voc_v = models.TextField(blank=True, null=True)
    isc_a = models.TextField(blank=True, null=True)
    efficiency = models.TextField(blank=True, null=True)
    phase_type = models.TextField(blank=True, null=True)
    warranty_years = models.TextField(blank=True, null=True)
    voltage = models.TextField(blank=True, null=True)
    dod = models.TextField(blank=True, null=True)
    cycle_life = models.TextField(blank=True, null=True)
    supplier = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
