# Generated by Django 4.2.2 on 2023-07-04 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0026_alter_product_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extraimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product'),
        ),
    ]
