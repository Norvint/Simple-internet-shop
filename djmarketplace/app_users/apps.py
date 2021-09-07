from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppUserConfig(AppConfig):
    name = 'app_users'
    verbose_name = _('users')

    def ready(self):
        import app_users.signals.handlers