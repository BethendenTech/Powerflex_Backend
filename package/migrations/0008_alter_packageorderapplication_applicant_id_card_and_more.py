# Generated by Django 5.1.4 on 2025-02-18 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0007_packageorder_packageorderapplication'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packageorderapplication',
            name='applicant_id_card',
            field=models.FileField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='packageorderapplication',
            name='bank_statements',
            field=models.FileField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='packageorderapplication',
            name='company_registration_document',
            field=models.FileField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='packageorderapplication',
            name='recent_utility_bill',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
