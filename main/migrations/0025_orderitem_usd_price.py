# Generated by Django 5.0.1 on 2024-03-03 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_order_total_amount_order_total_usd_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='usd_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
