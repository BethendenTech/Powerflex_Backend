# Generated by Django 5.1.4 on 2025-02-15 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0004_packageproducts'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PackageProducts',
            new_name='PackageProduct',
        ),
    ]
