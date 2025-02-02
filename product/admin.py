from django.contrib import admin
from .models import Category, Product, Brand, ApplianceCategory, Appliance, Band


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Band)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["name", "hours_supply", "price", "tariff"]
    search_fields = ["name", "hours_supply", "price", "tariff"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "brand", "price_usd", "capacity_w", "supplier"]
    list_filter = ["category", "brand", "price_usd", "capacity_w", "supplier"]
    search_fields = [
        "name",
        "category__name",
        "brand__name",
        "price_usd",
        "capacity_w",
        "supplier",
    ]


@admin.register(ApplianceCategory)
class ApplianceCategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Appliance)
class ApplianceAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "power_w"]
    list_filter = ["category"]
    search_fields = ["name", "category__name", "power_w"]
