# Generated by Django 4.1.3 on 2023-02-26 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_order_transaction_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='phone',
            field=models.EmailField(default='', max_length=200, null=True),
        ),
    ]
