# Generated by Django 5.0.7 on 2024-12-12 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_uploadedfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotebusiness',
            name='applicant_id_card',
            field=models.CharField(null=True),
        ),
        migrations.AlterField(
            model_name='quotebusiness',
            name='bank_statements',
            field=models.CharField(null=True),
        ),
        migrations.AlterField(
            model_name='quotebusiness',
            name='company_registration_document',
            field=models.CharField(null=True),
        ),
        migrations.AlterField(
            model_name='quotebusiness',
            name='recent_utility_bill',
            field=models.CharField(null=True),
        ),
    ]
