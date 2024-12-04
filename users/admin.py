from django.contrib import admin
from .models import UserDetail, Quote

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
