from django.db import models

class Settings(models.Model):
    vat = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    profit_margin = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    installation_margin = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return "Site Settings"

    class Meta:
        verbose_name = "Settings"
        verbose_name_plural = "Settings"