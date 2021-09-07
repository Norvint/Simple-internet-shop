from django.db.models.signals import pre_save
from django.dispatch import receiver

from app_goods.models import Order
from app_users.models import UserStatus


@receiver(pre_save, sender=Order)
def update_sums(sender, instance: Order, **kwargs):
    if not instance.score_accrued:
        instance.user.profile.score += instance.total_sum / 100
        available_statuses = UserStatus.objects.filter(scores_needed__lte=instance.user.profile.score)
        if len(available_statuses) > 1 and available_statuses.last() != instance.user.profile.status:
            instance.user.profile.status = available_statuses.last()
        instance.user.profile.save()
        instance.score_accrued = True
