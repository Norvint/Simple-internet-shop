# Generated by Django 3.1.3 on 2021-08-15 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0005_profile_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userstatus',
            options={'verbose_name': 'Статус пользователя', 'verbose_name_plural': 'Статусы пользователей'},
        ),
    ]
