# Generated by Django 5.1.4 on 2025-01-14 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_alter_address_pincode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='street_address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]