# Generated by Django 5.0.7 on 2024-12-07 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_quoteappliance'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='is_finance',
            field=models.BooleanField(null=True),
        ),
    ]