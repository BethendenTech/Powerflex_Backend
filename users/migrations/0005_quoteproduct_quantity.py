# Generated by Django 5.0.7 on 2024-12-04 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_quote_additional_info_quote_battery_autonomy_days_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quoteproduct',
            name='quantity',
            field=models.FloatField(null=True),
        ),
    ]