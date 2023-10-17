# Generated by Django 4.2.5 on 2023-10-14 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_rename_ordernumber_order_rename_orders_orderdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderdate', models.DateField(auto_now_add=True)),
                ('orderstatus', models.CharField(default='pending', max_length=200)),
                ('ordertype', models.CharField(max_length=200)),
                ('quantity', models.PositiveIntegerField()),
                ('finalprice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.address')),
            ],
        ),
        migrations.RenameField(
            model_name='order',
            old_name='Slno',
            new_name='slno',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='total_amount',
            new_name='totalamount',
        ),
        migrations.RemoveField(
            model_name='order',
            name='order',
        ),
        migrations.DeleteModel(
            name='Orderdetails',
        ),
        migrations.AddField(
            model_name='orders_details',
            name='ordernumber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.order'),
        ),
        migrations.AddField(
            model_name='orders_details',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.products'),
        ),
        migrations.AddField(
            model_name='orders_details',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.customers'),
        ),
    ]