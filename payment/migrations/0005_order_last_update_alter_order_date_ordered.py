# Generated by Django 5.1.4 on 2025-01-31 09:08

import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_rename_products_orderitem_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='last_update',
            field=django_jalali.db.models.jDateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_ordered',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True),
        ),
    ]
