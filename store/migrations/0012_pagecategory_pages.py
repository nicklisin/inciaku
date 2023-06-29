# Generated by Django 4.1.3 on 2023-04-10 03:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_orderitem_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Pages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('title', models.CharField(max_length=300)),
                ('description', models.CharField(max_length=600, null=True)),
                ('body', models.TextField(null=True)),
                ('url', models.SlugField()),
                ('order', models.IntegerField(default=1)),
                ('in_main_menu', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.pagecategory')),
            ],
        ),
    ]