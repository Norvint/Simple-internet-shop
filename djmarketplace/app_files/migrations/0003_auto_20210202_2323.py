# Generated by Django 3.1.3 on 2021-02-02 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_files', '0002_auto_20210202_2252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.IntegerField(verbose_name='Артикул'),
        ),
    ]
