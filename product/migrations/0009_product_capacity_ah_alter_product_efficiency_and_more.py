# Generated by Django 5.1.4 on 2025-02-05 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_band_tariff'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='capacity_ah',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='efficiency',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='voltage',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
