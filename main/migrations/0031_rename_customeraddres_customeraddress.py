# Generated by Django 5.0.1 on 2024-03-06 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_customeraddres_delete_customeraddress'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustomerAddres',
            new_name='CustomerAddress',
        ),
    ]