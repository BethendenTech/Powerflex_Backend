# Generated by Django 5.0.7 on 2024-11-05 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vat', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('profit_margin', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('installation_margin', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
            ],
            options={
                'verbose_name': 'Settings',
                'verbose_name_plural': 'Settings',
            },
        ),
    ]
