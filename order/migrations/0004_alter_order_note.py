# Generated by Django 4.2.5 on 2024-01-30 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_order_email_address_alter_order_note_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='note',
            field=models.TextField(blank=True, max_length=200),
        ),
    ]