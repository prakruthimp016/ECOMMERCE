# Generated by Django 5.1.4 on 2025-01-08 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_alter_orderitem_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.RemoveField(
            model_name='address',
            name='user',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='user',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserModel',
        ),
    ]