from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from app_goods.models import Cart
from app_users.models import Profile, UserStatus


@receiver(post_save, sender=User)
def check_for_cart(sender, instance: User, **kwargs):
    try:
        Cart.objects.get(user=instance)
    except Cart.DoesNotExist:
        Cart.objects.create(user=instance, items=0, total_sum=0)


@receiver(pre_save, sender=Profile)
def set_status(sender, instance: Profile, **kwargs):
    if instance.status is None and instance.score == 0:
        try:
            instance.status = UserStatus.objects.get(title='Newbee')
        except UserStatus.DoesNotExist:
            instance.status = UserStatus.objects.create(title='Newbee', scores_needed='0')