# Generated by Django 3.1.3 on 2021-07-29 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_goods', '0003_auto_20210729_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='items',
            field=models.PositiveIntegerField(default=0, verbose_name='items quantity'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='total_sum',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='total sum'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_sum',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='total sum'),
        ),
    ]
