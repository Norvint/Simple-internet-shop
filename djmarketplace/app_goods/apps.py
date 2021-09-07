from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppGoodsConfig(AppConfig):
    name = 'app_goods'
    verbose_name = _('goods')

    def ready(self):
        import app_goods.signals.handlers
