# Generated by Django 4.2.5 on 2024-01-30 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_alter_order_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(default=None, max_length=20),
        ),
    ]
