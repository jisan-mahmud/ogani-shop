# Generated by Django 4.2.5 on 2024-01-23 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_alter_product_created_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='views',
            field=models.IntegerField(auto_created=True, default=0),
        ),
    ]
