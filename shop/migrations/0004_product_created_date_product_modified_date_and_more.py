# Generated by Django 4.2.5 on 2024-01-23 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_remove_product_created_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='created_date',
            field=models.DateTimeField(default='2006-10-25 14:30:59'),
        ),
        migrations.AddField(
            model_name='product',
            name='modified_date',
            field=models.DateTimeField(default='2006-10-25 14:30:59'),
        ),
        migrations.AddField(
            model_name='product',
            name='views',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
