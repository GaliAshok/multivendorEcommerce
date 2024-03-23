# Generated by Django 5.0.1 on 2024-03-12 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_product_published_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='customer_image',
        ),
        migrations.AddField(
            model_name='vendor',
            name='profile_img',
            field=models.ImageField(null=True, upload_to='seller_imgs/'),
        ),
    ]
