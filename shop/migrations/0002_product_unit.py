# Generated by Django 4.2.5 on 2024-01-21 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='unit',
            field=models.CharField(default='kg', max_length=10),
        ),
    ]