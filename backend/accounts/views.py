from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages
from . import views
import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from django.views.decorators.cache import never_cache
from packages.models import Package
from subscriptions.models import Subscription
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum
from .models import MT5Account
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse



User = get_user_model()


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile_no = request.POST.get("mobile_no")
        password = request.POST.get('password')

        # First user becomes superadmin
        if User.objects.filter(role="superadmin").exists():
            assigned_role = "user"
        else:
            assigned_role = "superadmin"

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            mobile_no=mobile_no,
            role=assigned_role
        )

        user.save()

        return redirect('login')


    return render(request, 'accounts/register.html')


def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.role == "superadmin":
                return redirect('superadmin_dashboard')
            elif user.role == "admin":
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')

        else:
            messages.error(request, "Invalid email or password")
            return redirect('login')

    return render(request, 'accounts/login.html')


@login_required(login_url='login')
@never_cache
def superadmin_dashboard(request):
 
    if request.user.role != "superadmin":
        request.session.flush() 
        return redirect('login')
    return render(request, 'accounts/superadmin_dashboard.html')


@login_required
def admin_dashboard(request):
    if request.user.role != "admin":
        return redirect('login')
    return render(request, 'accounts/admin_dashboard.html')


@login_required
def user_dashboard(request):
    is_expired = False

    sub = Subscription.objects.filter(user=request.user).last()

    if sub:
        print("END DATE:", sub.end_date)
        print("NOW:", timezone.now())

        if sub.end_date <= timezone.now():
            print("EXPIRED TRUE ✅")
            is_expired = True
        else:
            print("NOT EXPIRED ❌")

    else:
        print("NO SUB ❌")
        is_expired = True

    packages = Package.objects.all()

    return render(request, 'accounts/user_dashboard.html', {
        'is_expired': is_expired,
        'packages': packages
    })
@login_required
def profile(request):
    if request.user.is_superuser:
        return render(request, 'accounts/superadmin_profile.html')
    else:
        return render(request, 'accounts/user_profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user
        )
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'accounts/edit_profile.html', {'form': form})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()  # ✅ THIS SAVES PASSWORD TO DATABASE
            update_session_auth_hash(request, user)  # ✅ keeps user logged in
            messages.success(request, "Password changed successfully!")
            return redirect('profile')
        else:
            print(form.errors)  # 👈 Add this for debugging

    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = CustomUser.objects.get(email=email)

            otp = str(random.randint(100000, 999999))
            user.otp = otp
            user.save()

            send_mail(
                'Your OTP Code',
                f'Your OTP is {otp}',
                'monalir416@gmail.com',
                [email],
                fail_silently=False,
            )

            request.session['reset_email'] = email
            return redirect('verify_otp')

        except CustomUser.DoesNotExist:
            return render(request, 'accounts/forgot_password.html', {'error': 'Email not found'})
    return render(request, 'accounts/forgot_password.html')

def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        email = request.session.get('reset_email')

        user = CustomUser.objects.get(email=email)

        if user.otp == entered_otp:
            return redirect('reset_password')
        else:
            return render(request, 'accounts/verify_otp.html', {'error': 'Invalid OTP'})

    return render(request, 'accounts/verify_otp.html')


def reset_password(request):
    if request.method == "POST":
        new_password = request.POST.get('password')
        email = request.session.get('reset_email')

        if not email:
            messages.error(request, "Session expired. Please try again.")
            return redirect('forgot_password')

        try:
            user = CustomUser.objects.get(email=email)

            # 🔥 IMPORTANT LINE
            user.set_password(new_password)

            # clear otp
            user.otp = None
            user.save()

            # clear session
            del request.session['reset_email']

            messages.success(request, "Password changed successfully!")
            return redirect('login')

        except CustomUser.DoesNotExist:
            messages.error(request, "User not found!")
            return redirect('forgot_password')

    return render(request, 'accounts/reset_password.html')

def user_packages(request):
    packages = Package.objects.all()   # 🔥 fetch all packages

    return render(request, 'accounts/user_packages.html', {
        'packages': packages
    })
    
def subscription_expired(request):
    return render(request, 'subscriptions/expired.html')

def superadmin_dashboard(request):

    # ✅ Total Users (only normal users)
    total_users = CustomUser.objects.filter(role='user').count()

    # ✅ Active Subscriptions (Orders)
    total_orders = Subscription.objects.filter(is_active=True).count()

    # ✅ Revenue (sum of plan price)
    total_revenue = Subscription.objects.filter(is_active=True).aggregate(
        total=Sum('plan__price')
    )['total'] or 0

    # ✅ Active Users (who purchased plan)
    active_users = Subscription.objects.filter(
        end_date__gt=timezone.now()
    ).values('user').distinct().count()

    context = {
        'total_users': total_users,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'active_users': active_users,   # optional
    }

    return render(request, 'accounts/superadmin_dashboard.html', context)


def notifications_view(request):

    yesterday = timezone.now() - timedelta(days=1)

    # 👤 Login Notifications
    recent_logins = CustomUser.objects.filter(
        last_login__gte=yesterday,
        role='user'
    ).order_by('-last_login')

    # 💰 Payment Notifications
    recent_payments = Subscription.objects.filter(
        is_active=True,
        start_date__gte=yesterday
    ).select_related('user', 'plan').order_by('-start_date')
    
           #✅ Mark as seen
    request.session['last_seen_notifications'] = timezone.now().isoformat()
    
    context = {
        'recent_logins': recent_logins,
        'recent_payments': recent_payments,
    }

    return render(request, 'accounts/notifications.html', context)


