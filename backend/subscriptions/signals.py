from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from .models import Subscription
from packages.models import Package

User = get_user_model()

@receiver(post_save, sender=User)
def create_trial_subscription(sender, instance, created, **kwargs):
    if created:
        # ✅ SAFE: auto create if not exists
        trial_package, created = Package.objects.get_or_create(
            name="trial_plan",
            defaults={
                "price": 0,
                "duration": 7
            }
        )

        Subscription.objects.create(
            user=instance,
            plan=trial_package
        )