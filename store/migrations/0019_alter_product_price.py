# Generated by Django 4.1.3 on 2023-05-09 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_product_art_code_product_capacity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True),
        ),
    ]