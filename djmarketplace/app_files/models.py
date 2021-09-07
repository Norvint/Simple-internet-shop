import os
from datetime import datetime

from django.conf.global_settings import MEDIA_ROOT
from django.db import models

from django.utils.deconstruct import deconstructible

@deconstructible
class UploadToPathAndRename(object):

    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        filename = f'{datetime.now().strftime("%m%d%Y-%H-%M-%S")}_{filename}'
        return os.path.join(MEDIA_ROOT, self.sub_path, filename)


class File(models.Model):
    file = models.FileField('Файл', upload_to=UploadToPathAndRename('files'))
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

