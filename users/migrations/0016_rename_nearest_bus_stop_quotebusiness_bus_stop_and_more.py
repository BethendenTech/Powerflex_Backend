# Generated by Django 5.0.7 on 2024-12-13 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_alter_quotebusiness_applicant_id_card_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quotebusiness',
            old_name='nearest_bus_stop',
            new_name='bus_stop',
        ),
        migrations.RenameField(
            model_name='quotebusiness',
            old_name='role',
            new_name='business_address',
        ),
        migrations.RenameField(
            model_name='quotebusiness',
            old_name='street_name',
            new_name='business_role',
        ),
        migrations.RenameField(
            model_name='quoteindividual',
            old_name='nearest_bus_stop',
            new_name='bus_stop',
        ),
        migrations.RenameField(
            model_name='quoteindividual',
            old_name='street_name',
            new_name='business_address',
        ),
        migrations.RemoveField(
            model_name='quoteindividual',
            name='work_address',
        ),
        migrations.AddField(
            model_name='quotebusiness',
            name='city',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='quotebusiness',
            name='email',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='quotebusiness',
            name='how_heard_about',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='quotebusiness',
            name='landmark',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='quotebusiness',
            name='occupation',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='quotebusiness',
            name='reference_phone1',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='quotebusiness',
            name='reference_phone2',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='quotebusiness',
            name='street_address',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='quotebusiness',
            name='town',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='quoteindividual',
            name='business_name',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='quoteindividual',
            name='business_role',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='quoteindividual',
            name='bvn',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='quoteindividual',
            name='email',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='quoteindividual',
            name='other_role',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='quoteindividual',
            name='reference_phone1',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='quoteindividual',
            name='reference_phone2',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='quoteindividual',
            name='street_address',
            field=models.CharField(null=True),
        ),
    ]