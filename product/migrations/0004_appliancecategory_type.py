# Generated by Django 5.0.7 on 2024-12-05 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_appliance_power_w'),
    ]

    operations = [
        migrations.AddField(
            model_name='appliancecategory',
            name='type',
            field=models.CharField(blank=True, null=True),
        ),
    ]
