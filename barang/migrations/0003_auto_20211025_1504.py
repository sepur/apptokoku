# Generated by Django 3.1.2 on 2021-10-25 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('barang', '0002_auto_20211025_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemorder',
            name='item_order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='barang.order'),
        ),
    ]
