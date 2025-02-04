# Generated by Django 5.0.7 on 2024-12-08 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_quote_is_finance'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quote',
            old_name='installer_cost',
            new_name='installation_and_cabling',
        ),
        migrations.RenameField(
            model_name='quote',
            old_name='total_battery_cost_naira',
            new_name='installer_commission',
        ),
        migrations.RenameField(
            model_name='quote',
            old_name='total_battery_cost_usd',
            new_name='installer_commission_amount',
        ),
        migrations.RenameField(
            model_name='quote',
            old_name='total_inverter_cost_naira',
            new_name='total_equipments',
        ),
        migrations.RenameField(
            model_name='quote',
            old_name='total_inverter_cost_usd',
            new_name='total_vat',
        ),
        migrations.RenameField(
            model_name='quote',
            old_name='total_panel_cost_naira',
            new_name='vat',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='number_of_batteries',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='number_of_inverters',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='number_of_panels',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='total_panel_cost_usd',
        ),
    ]
