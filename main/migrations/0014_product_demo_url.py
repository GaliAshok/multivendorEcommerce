# Generated by Django 5.0.1 on 2024-02-20 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_product_image_product_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='demo_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
