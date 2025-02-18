from django.db import models
from product.models import Appliance


class Package(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="package_images/", blank=True, null=True)
    runtime = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # Define a ManyToMany relationship with Appliance through PackageAppliances
    appliances = models.ManyToManyField(
        Appliance, through="PackageAppliances", related_name="packages"
    )

    def __str__(self):
        return self.name


class PackageAppliances(models.Model):
    package = models.ForeignKey(
        Package, on_delete=models.CASCADE, related_name="package_appliances"
    )
    appliance = models.ForeignKey(
        Appliance, on_delete=models.CASCADE, related_name="appliance_packages"
    )

    # Optional: Add additional fields to the join table if needed
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return (
            f"{self.package.name} - {self.appliance.name} (Quantity: {self.quantity})"
        )


class PackageProduct(models.Model):
    package = models.ForeignKey(
        Package, on_delete=models.CASCADE, related_name="package_products"
    )
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name


class PackageOrder(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        CANCELLED = "cancelled", "Cancelled"
        APPROVED = "approved", "Approved"

    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    is_finance = models.BooleanField(null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        help_text="Status of the quote (e.g., Pending, Paid, Cancelled, Approved)",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PackageOrderApplication(models.Model):
    packageOrder = models.ForeignKey(PackageOrder, on_delete=models.CASCADE)
    application_type = models.CharField(null=True)
    bvn = models.CharField(null=True)
    other_role = models.CharField(null=True)
    first_name = models.CharField(null=True)
    last_name = models.CharField(null=True)
    house_number = models.CharField(null=True)
    street_address = models.CharField(null=True)
    landmark = models.CharField(null=True)
    bus_stop = models.CharField(null=True)
    occupation = models.CharField(null=True)
    business_role = models.CharField(null=True)
    business_name = models.CharField(null=True)
    business_address = models.CharField(null=True)
    town = models.CharField(null=True)
    city = models.CharField(null=True)
    state = models.CharField(null=True)
    lga = models.CharField(null=True)
    email = models.CharField(null=True)
    phone_number = models.CharField(null=True)
    reference_phone1 = models.CharField(null=True)
    reference_phone2 = models.CharField(null=True)
    how_heard_about = models.TextField(null=True)
    applicant_id_card = models.CharField(null=True)
    company_registration_document = models.CharField(null=True)
    bank_statements = models.CharField(null=True)
    recent_utility_bill = models.CharField(null=True)
