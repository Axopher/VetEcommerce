# Generated by Django 4.2.2 on 2023-07-03 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_alter_shippingaddress_latitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='product/product-1.png', null=True, upload_to='images/product/'),
        ),
    ]
