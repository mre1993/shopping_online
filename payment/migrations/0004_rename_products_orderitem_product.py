# Generated by Django 5.1.4 on 2025-01-31 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_order_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='products',
            new_name='product',
        ),
    ]
