# Generated by Django 5.0.7 on 2024-11-19 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0002_settings_installer_commission'),
    ]

    operations = [
        migrations.RenameField(
            model_name='settings',
            old_name='profit_margin',
            new_name='profit_margin_financing',
        ),
        migrations.AddField(
            model_name='settings',
            name='profit_margin_outright',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
    ]
