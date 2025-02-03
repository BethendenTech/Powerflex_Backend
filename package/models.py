from django.db import models
from product.models import Appliance

class Package(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    # Define a ManyToMany relationship with Appliance through PackageAppliances
    appliances = models.ManyToManyField(Appliance, through='PackageAppliances', related_name='packages')

    def __str__(self):
        return self.name

class PackageAppliances(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='package_appliances')
    appliance = models.ForeignKey(Appliance, on_delete=models.CASCADE, related_name='appliance_packages')

    # Optional: Add additional fields to the join table if needed
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.package.name} - {self.appliance.name} (Quantity: {self.quantity})"