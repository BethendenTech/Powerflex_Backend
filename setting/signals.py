def create_default_settings(sender, **kwargs):
    from .models import Settings
    if not Settings.objects.exists():
        Settings.objects.create(vat=7.5, profit_margin=20.00, installation_margin=15.00)
