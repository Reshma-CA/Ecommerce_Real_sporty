# Generated by Django 4.2.5 on 2023-10-14 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_orders_details_rename_slno_order_slno_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='slno',
        ),
    ]
