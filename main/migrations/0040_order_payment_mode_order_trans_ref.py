# Generated by Django 5.0.1 on 2024-03-20 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0039_productcategory_cat_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_mode',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='trans_ref',
            field=models.TextField(blank=True, null=True),
        ),
    ]
