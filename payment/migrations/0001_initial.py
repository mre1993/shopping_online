# Generated by Django 5.1.4 on 2024-12-23 12:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipping_full_name', models.CharField(max_length=250)),
                ('shipping_email', models.CharField(max_length=250)),
                ('shipping_phone', models.CharField(blank=True, max_length=25)),
                ('shipping_address1', models.CharField(blank=True, max_length=200)),
                ('shipping_address2', models.CharField(blank=True, max_length=200)),
                ('shipping_city', models.CharField(blank=True, max_length=25)),
                ('shipping_state', models.CharField(blank=True, max_length=25)),
                ('shipping_zipcode', models.CharField(blank=True, max_length=25)),
                ('shipping_country', models.CharField(default='IRAN', max_length=25)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Shipping Address',
            },
        ),
    ]
