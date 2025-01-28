from django.contrib import admin
from django import forms
from .models import Settings


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = "__all__"
        labels = {
            "installation_margin": "Cabling And Installation Cost",
            "installer_commission": "Installer Margin",
        }


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    form = SettingsForm
    list_display = [
        "vat",
        "profit_margin_outright",
        "profit_margin_financing",
        "installation_margin",
        "installer_commission",
        "exchange_rate",
    ]

    def has_add_permission(self, request):
        # Prevent adding more than one instance
        return not Settings.objects.exists()
