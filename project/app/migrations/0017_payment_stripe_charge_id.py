# Generated by Django 5.1.4 on 2025-01-11 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_address_user_order_user_orderitem_user_payment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='Stripe_charge_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
