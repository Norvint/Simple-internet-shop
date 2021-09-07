# Generated by Django 3.1.3 on 2021-08-15 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_goods', '0008_auto_20210815_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items_in_cart', to='app_goods.cart', verbose_name='cart'),
        ),
        migrations.AlterField(
            model_name='itemimage',
            name='item',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='app_goods.item', verbose_name='item'),
        ),
        migrations.AlterField(
            model_name='iteminshop',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items_in_shop', to='app_goods.item', verbose_name='item'),
        ),
        migrations.AlterField(
            model_name='iteminshop',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items_in_shop', to='app_goods.shop', verbose_name='shop'),
        ),
    ]