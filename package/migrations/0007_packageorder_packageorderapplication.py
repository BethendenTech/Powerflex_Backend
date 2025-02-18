# Generated by Django 5.1.4 on 2025-02-18 07:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0006_alter_packageproduct_package'),
    ]

    operations = [
        migrations.CreateModel(
            name='PackageOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=20)),
                ('is_finance', models.BooleanField(null=True)),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('paid', 'Paid'), ('cancelled', 'Cancelled'), ('approved', 'Approved')], default='pending', help_text='Status of the quote (e.g., Pending, Paid, Cancelled, Approved)', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='package.package')),
            ],
        ),
        migrations.CreateModel(
            name='PackageOrderApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application_type', models.CharField(null=True)),
                ('bvn', models.CharField(null=True)),
                ('other_role', models.CharField(null=True)),
                ('first_name', models.CharField(null=True)),
                ('last_name', models.CharField(null=True)),
                ('house_number', models.CharField(null=True)),
                ('street_address', models.CharField(null=True)),
                ('landmark', models.CharField(null=True)),
                ('bus_stop', models.CharField(null=True)),
                ('occupation', models.CharField(null=True)),
                ('business_role', models.CharField(null=True)),
                ('business_name', models.CharField(null=True)),
                ('business_address', models.CharField(null=True)),
                ('town', models.CharField(null=True)),
                ('city', models.CharField(null=True)),
                ('state', models.CharField(null=True)),
                ('lga', models.CharField(null=True)),
                ('email', models.CharField(null=True)),
                ('phone_number', models.CharField(null=True)),
                ('reference_phone1', models.CharField(null=True)),
                ('reference_phone2', models.CharField(null=True)),
                ('how_heard_about', models.TextField(null=True)),
                ('applicant_id_card', models.CharField(null=True)),
                ('company_registration_document', models.CharField(null=True)),
                ('bank_statements', models.CharField(null=True)),
                ('recent_utility_bill', models.CharField(null=True)),
                ('packageOrder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='package.packageorder')),
            ],
        ),
    ]
