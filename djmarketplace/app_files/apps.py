from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppFilesConfig(AppConfig):
    name = 'app_files'
    verbose_name = _('files')
