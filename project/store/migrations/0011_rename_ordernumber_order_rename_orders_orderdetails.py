# Generated by Django 4.2.5 on 2023-10-14 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_remove_orders_cart_remove_orders_ordernumber_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ordernumber',
            new_name='Order',
        ),
        migrations.RenameModel(
            old_name='Orders',
            new_name='Orderdetails',
        ),
    ]
