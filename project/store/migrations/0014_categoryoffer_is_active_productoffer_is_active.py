# Generated by Django 4.2.5 on 2023-10-20 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_remove_order_slno'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoryoffer',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='productoffer',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
