from .models import Subscription
from django.utils import timezone

class SubscriptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        request.is_expired = False   # ✅ default

        if request.user.is_authenticated:
            sub = Subscription.objects.filter(user=request.user).last()

            if sub and sub.end_date <= timezone.now():
                request.is_expired = True   # ✅ set flag (NO redirect)

        return self.get_response(request)