from django.contrib import admin

from .models import Settings

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ['vat', 'profit_margin', 'installation_margin']

    def has_add_permission(self, request):
        # Prevent adding more than one instance
        return not Settings.objects.exists()
