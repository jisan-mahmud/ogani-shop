# Generated by Django 4.2.5 on 2024-01-23 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_product_shipping_alter_product_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.DecimalField(decimal_places=2, default=True, max_digits=5),
        ),
    ]
