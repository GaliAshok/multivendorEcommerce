# Generated by Django 5.0.1 on 2024-03-06 14:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_alter_customeraddress_customer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customeraddress',
            options={'verbose_name_plural': 'Customer Addresses'},
        ),
        migrations.AlterField(
            model_name='customeraddress',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_addresses', to='main.customer'),
        ),
    ]
