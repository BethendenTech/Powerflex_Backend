# Generated by Django 5.1.4 on 2025-01-30 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_band'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='capacity_w',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
