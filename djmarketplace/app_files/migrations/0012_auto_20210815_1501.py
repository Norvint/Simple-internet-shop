# Generated by Django 3.1.3 on 2021-08-15 12:01
import os

from django.conf.global_settings import MEDIA_ROOT

import app_files.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_files', '0011_auto_20210729_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to=app_files.models.UploadToPathAndRename(os.path.join(MEDIA_ROOT, 'files')),
                                   verbose_name='Файл'),
        ),
    ]
