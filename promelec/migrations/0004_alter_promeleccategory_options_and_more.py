# Generated by Django 5.0.6 on 2024-05-11 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promelec', '0003_promelecproduct_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='promeleccategory',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterField(
            model_name='promeleccategory',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='promeleccategory',
            unique_together={('name', 'parent')},
        ),
    ]
