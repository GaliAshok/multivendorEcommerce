# Generated by Django 5.0.1 on 2024-03-16 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0037_remove_vendor_customer_image_vendor_profile_img'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productrating',
            old_name='ratings',
            new_name='rating',
        ),
    ]