# Generated by Django 5.0.1 on 2024-03-02 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_alter_product_downloads'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='usd_price',
            field=models.DecimalField(decimal_places=2, default=80, max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
