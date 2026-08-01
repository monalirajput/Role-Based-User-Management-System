from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .models import Subscription, UserSubscription
from packages.models import Package
import razorpay
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect
# ✅ CHECK SUBSCRIPTION
def check_subscription(request):
    sub = Subscription.objects.get(user=request.user)

    return JsonResponse({
        "plan": sub.plan_name,
        "end_date": sub.end_date,
        "expired": sub.is_expired()
    })


# ✅ EXPIRED PAGE
def subscription_expired(request):
    return render(request, 'subscriptions/expired.html')


# ✅ CREATE ORDER (FIXED)
def create_order(request):
    if request.method == "POST":
        try:
            plan_id = request.POST.get("plan_id")
            plan = Package.objects.get(id=plan_id)

            # 🔥 Convert Decimal → int (IMPORTANT)
            amount = int(float(plan.price) * 100)

            client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
            )

            order = client.order.create({
                "amount": amount,
                "currency": "INR",
                "payment_capture": 1
            })

            return JsonResponse({
                "order_id": order["id"],
                "amount": amount,
                "key": settings.RAZORPAY_KEY_ID,   # ✅ correct
                "plan_id": plan.id
            })

        except Exception as e:
            print("CREATE ORDER ERROR:", e)
            return JsonResponse({"error": str(e)}, status=500)


# ✅ VERIFY PAYMENT
from django.utils import timezone
from datetime import timedelta
from subscriptions.models import Subscription

def verify_payment(request):
    if request.method == "POST":
        try:
            user = request.user
            plan_id = request.POST.get("plan_id")
            payment_id = request.POST.get("payment_id")
            order_id = request.POST.get("order_id")

            plan = Package.objects.get(id=plan_id)

            # ✅ Save payment history
            UserSubscription.objects.create(
                user=user,
                plan=plan,
                payment_id=payment_id,
                order_id=order_id,
                status="Success"
            )

            # 🔥 UPDATE MAIN SUBSCRIPTION (IMPORTANT)
            subscription, created = Subscription.objects.get_or_create(user=user)

            subscription.plan = plan
            subscription.start_date = timezone.now()
            subscription.end_date = timezone.now() + timedelta(days=plan.duration)
            subscription.save()

            print("✅ PAYMENT SAVED + SUBSCRIPTION UPDATED")

            return JsonResponse({"status": "success"})

        except Exception as e:
            print("VERIFY ERROR:", e)
            return JsonResponse({"error": str(e)}, status=500)
        
from django.contrib.admin.views.decorators import staff_member_required
from .models import Subscription


def transactions_view(request):

    from .models import UserSubscription

    transactions = UserSubscription.objects.select_related('user', 'plan').all().order_by('-id')

    return render(request, 'accounts/transactions.html', {
        'transactions': transactions
    })