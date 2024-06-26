# Generated by Django 5.0.6 on 2024-05-12 19:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promelec', '0005_promelecbrand_alter_promelecproduct_brand'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromelecOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('quantity', models.PositiveIntegerField(verbose_name='Количество')),
                ('warehouse', models.CharField(max_length=255, verbose_name='Склад')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('state', models.CharField(choices=[('SOLD_VERIFICATION', 'Проверка продажи'), ('SOLD', 'Продан'), ('RETURNED', 'Возвращен'), ('RESTOCK_VERIFICATION', 'Проверка пополнения'), ('RESTOCKED', 'Пополнен')], default='SOLD_VERIFICATION', max_length=20, verbose_name='Статус')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='promelec.promelecproduct', verbose_name='Товар')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
