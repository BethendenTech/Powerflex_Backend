from django.contrib import admin
from .models import (
    UserDetail,
    Quote,
    QuoteAppliance,
    QuoteProduct,
    QuoteApplication,
)


# Reusable mixin for displaying quote number
class QuoteNumberMixin:
    def quote_number(self, obj):
        return obj.quote.quote_number if obj.quote else "N/A"

    quote_number.short_description = "Quote Number"


# Register your models here.
@admin.register(UserDetail)
class UserDetailAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone_number")
    search_fields = ("name",)
    list_filter = ("email",)
    ordering = ("name",)


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = [
        "quote_number",
        "user",
        "electricity_spend",
        "price_band",
        "total_load_kwh",
        "total_equipments",
        "total_vat",
        "installer_commission_amount",
        "status",
        "created_at",
    ]
    list_filter = [
        "quote_number",
        "user",
        "electricity_spend",
        "price_band",
        "total_load_kwh",
        "total_equipments",
        "total_vat",
        "installer_commission_amount",
        "status",
        "created_at",
    ]
    search_fields = [
        "quote_number",
        "user__name",
        "electricity_spend",
        "price_band",
        "total_load_kwh",
        "total_equipments",
        "total_vat",
        "installer_commission_amount",
        "status",
        "created_at",
    ]


@admin.register(QuoteAppliance)
class QuoteApplianceAdmin(QuoteNumberMixin, admin.ModelAdmin):
    list_display = ["quote_number", "appliance", "quantity", "usage"]
    list_filter = ["quote", "appliance", "quantity", "usage"]
    search_fields = ["quote__quote_number", "appliance__name", "quantity", "usage"]


@admin.register(QuoteProduct)
class QuoteProductAdmin(QuoteNumberMixin, admin.ModelAdmin):
    list_display = ["quote_number", "product", "quantity", "capacity_w", "price_usd"]
    list_filter = ["quote", "product", "quantity", "capacity_w", "price_usd"]
    search_fields = [
        "quote__quote_number",
        "product__name",
        "quantity",
        "capacity_w",
        "price_usd",
    ]


@admin.register(QuoteApplication)
class QuoteApplicationAdmin(QuoteNumberMixin, admin.ModelAdmin):
    list_display = [
        "quote_number",
        "application_type",
        "bvn",
        "first_name",
        "last_name",
        "phone_number",
        "email",
        "street_address",
        "occupation",
        "business_address",
        "how_heard_about",
    ]
    list_filter = [
        "quote",
        "application_type",
        "bvn",
        "first_name",
        "last_name",
        "phone_number",
        "email",
        "street_address",
        "occupation",
        "business_address",
        "how_heard_about",
    ]
    search_fields = [
        "quote__quote_number",
        "application_type",
        "bvn",
        "first_name",
        "last_name",
        "phone_number",
        "email",
        "street_address",
        "occupation",
        "business_address",
        "how_heard_about",
    ]
