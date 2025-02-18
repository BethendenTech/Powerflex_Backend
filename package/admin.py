from django.contrib import admin
from .models import (
    Package,
    PackageAppliances,
    PackageProduct,
    PackageOrder,
    PackageOrderApplication,
)

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


@admin.register(PackageOrder)
class PackageOrderAdmin(admin.ModelAdmin):
    list_display = ("package", "name", "email", "phone_number", "total_price")
    list_filter = ("package", "name", "email", "phone_number", "total_price")
    search_fields = ("package__name", "name", "email", "phone_number")


@admin.register(PackageOrderApplication)
class PackageOrderApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "packageOrder",
        "application_type",
        "bvn",
        "other_role",
        "first_name",
        "last_name",
    )
    list_filter = (
        "packageOrder",
        "application_type",
        "bvn",
        "other_role",
        "first_name",
        "last_name",
    )
    search_fields = (
        "packageOrder__id",
        "application_type",
        "bvn",
        "other_role",
        "first_name",
        "last_name",
    )
