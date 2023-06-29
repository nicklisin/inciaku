# Generated by Django 4.1.3 on 2023-04-10 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_pagecategory_pages'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pagecategory',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AddField(
            model_name='pagecategory',
            name='url',
            field=models.SlugField(default='', null=True),
        ),
    ]
