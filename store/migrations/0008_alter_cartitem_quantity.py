# Generated by Django 4.2.2 on 2023-06-14 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_rename_user_cart_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
