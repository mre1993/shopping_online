# Generated by Django 5.1.4 on 2024-12-22 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='old_cart',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
