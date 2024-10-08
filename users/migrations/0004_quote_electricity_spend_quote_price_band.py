# Generated by Django 4.2.16 on 2024-10-01 10:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_quote'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='electricity_spend',
            field=models.DecimalField(decimal_places=2, default=200000, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quote',
            name='price_band',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]
