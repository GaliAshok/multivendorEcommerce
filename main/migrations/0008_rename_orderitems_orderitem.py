# Generated by Django 5.0.1 on 2024-02-10 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_orderitems_product'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrderItems',
            new_name='OrderItem',
        ),
    ]
