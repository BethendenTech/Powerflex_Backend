from django.contrib import admin
from .models import (
    UserDetail,
    Quote,
    QuoteAppliance,
    QuoteProduct,
    QuoteApplication,
)

# Register your models here.


@admin.register(UserDetail)
class UserDetailAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone_number")
    search_fields = ("name",)
    list_filter = ("email",)
    ordering = ("name",)


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ["user", "quote_number", "electricity_spend", "price_band"]
    list_filter = ["user", "quote_number", "electricity_spend", "price_band"]
    search_fields = ["user__name", "quote_number", "electricity_spend", "price_band"]


@admin.register(QuoteAppliance)
class QuoteApplianceAdmin(admin.ModelAdmin):
    list_display = ["quote", "appliance", "quantity", "usage"]
    list_filter = ["quote", "appliance", "quantity", "usage"]
    search_fields = ["quote__quote_number", "appliance__name", "quantity", "usage"]


@admin.register(QuoteProduct)
class QuoteProductAdmin(admin.ModelAdmin):
    list_display = ["quote", "product", "quantity"]
    list_filter = ["quote", "product", "quantity"]
    search_fields = ["quote__quote_number", "product__name", "quantity"]


@admin.register(QuoteApplication)
class QuoteApplicationAdmin(admin.ModelAdmin):
    list_display = ["quote", "application_type", "first_name", "last_name"]
    list_filter = ["quote", "application_type", "first_name", "last_name"]
    search_fields = [
        "quote__quote_number",
        "application_type",
        "first_name",
        "last_name",
    ]
