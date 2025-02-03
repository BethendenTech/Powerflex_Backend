# Generated by Django 5.1.4 on 2025-02-03 06:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0008_band_tariff'),
    ]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PackageAppliances',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('appliance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appliance_packages', to='product.appliance')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='package_appliances', to='package.package')),
            ],
        ),
        migrations.AddField(
            model_name='package',
            name='appliances',
            field=models.ManyToManyField(related_name='packages', through='package.PackageAppliances', to='product.appliance'),
        ),
    ]
