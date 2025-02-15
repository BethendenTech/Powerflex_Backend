from django.contrib import admin
from .models import Package, PackageAppliances, PackageProduct

# Register your models here.


class PackageAppliancesInline(admin.TabularInline):  # or admin.StackedInline
    model = PackageAppliances
    extra = 1  # Number of empty forms to display for adding new related objects


class PackageProductInline(admin.TabularInline):  # or admin.StackedInline
    model = PackageProduct
    extra = 1  # Number of empty forms to display for adding new related objects


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "discount_price")
    list_filter = ("price", "discount_price")
    search_fields = ("name", "description")
    inlines = [
        PackageAppliancesInline,
        PackageProductInline,
    ]  # Add the inline for PackageAppliances
