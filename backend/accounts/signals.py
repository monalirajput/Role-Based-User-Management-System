from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from subscriptions.models import Subscription
from datetime import timedelta
from django.utils import timezone

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_subscription(sender, instance, created, **kwargs):
    if created:
        Subscription.objects.create(
            user=instance,
            plan_name="Free Trial",
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=15),
            is_active=True
        )