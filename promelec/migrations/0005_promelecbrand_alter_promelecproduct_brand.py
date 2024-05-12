# Generated by Django 5.0.6 on 2024-05-11 17:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promelec', '0004_alter_promeleccategory_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromelecBrand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Бренд',
                'verbose_name_plural': 'Бренды',
            },
        ),
        migrations.AlterField(
            model_name='promelecproduct',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='promelec.promelecbrand', verbose_name='Производитель'),
        ),
    ]