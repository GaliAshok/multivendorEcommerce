# Generated by Django 5.0.1 on 2024-02-28 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_orderitem_price_orderitem_qty'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.BooleanField(default=False),
        ),
    ]
