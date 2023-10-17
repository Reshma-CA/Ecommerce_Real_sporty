# Generated by Django 4.2.5 on 2023-10-08 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_wishlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZoomProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('original_image', models.ImageField(upload_to='products/')),
            ],
        ),
    ]