from django.contrib import admin
from .models import Package, PackageAppliances

# Register your models here.

class PackageAppliancesInline(admin.TabularInline):  # or admin.StackedInline
    model = PackageAppliances
    extra = 1  # Number of empty forms to display for adding new related objects

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount_price')
    list_filter = ('price', 'discount_price')
    search_fields = ('name', 'description')
    inlines = [PackageAppliancesInline]  # Add the inline for PackageAppliances

@admin.register(PackageAppliances)
class PackageAppliancesAdmin(admin.ModelAdmin):
    list_display = ('package', 'appliance', 'quantity')
    list_filter = ('package', 'appliance')
    search_fields = ('package__name', 'appliance__name')