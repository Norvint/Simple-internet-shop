from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserStatus(models.Model):
    title = models.CharField(_('title'), max_length=100)
    scores_needed = models.PositiveIntegerField(_('scores needed'))

    class Meta:
        verbose_name = 'Статус пользователя'
        verbose_name_plural = 'Статусы пользователей'

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('user'))
    city = models.CharField(_('city'), max_length=30, blank=True, null=True)
    phone_number = models.CharField(_('phone number'), max_length=30, blank=True, null=True)
    date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)
    balance = models.IntegerField(_('balance'), default=0)
    score = models.PositiveIntegerField(_('score'), default=0)
    status = models.ForeignKey(UserStatus, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('status'))

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def __str__(self):
        return f'{self.pk}'

