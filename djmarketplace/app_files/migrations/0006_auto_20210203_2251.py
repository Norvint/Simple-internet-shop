# Generated by Django 3.1.3 on 2021-02-03 19:51

import app_files.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_files', '0005_auto_20210203_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to=app_files.models.UploadToPathAndRename('/files'), verbose_name='Файл'),
        ),
    ]