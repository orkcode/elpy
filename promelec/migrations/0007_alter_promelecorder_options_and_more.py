# Generated by Django 5.0.6 on 2024-05-12 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promelec', '0006_promelecorder'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='promelecorder',
            options={'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterUniqueTogether(
            name='promelecorder',
            unique_together={('product', 'quantity', 'warehouse', 'price', 'created_at')},
        ),
    ]
