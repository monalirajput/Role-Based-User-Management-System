from django.shortcuts import render, redirect
from .models import SiteSetting
from django.contrib import messages


# ✅ DEFINE THIS FIRST
def get_setting():
    setting = SiteSetting.objects.first()
    if not setting:
        setting = SiteSetting.objects.create(site_name="My Website")
    return setting


# ✅ THEN USE IT
def general_settings(request):
    setting = get_setting()

    if request.method == "POST":

        if "general_submit" in request.POST:
            setting.site_name = request.POST.get("site_name")
            setting.email = request.POST.get("email")
            setting.phone = request.POST.get("phone")
            setting.timezone = request.POST.get("timezone")
            setting.save()
            messages.success(request, "Save settings successfully!")

        elif "seo_submit" in request.POST:
            setting.meta_title = request.POST.get("meta_title")
            setting.meta_description = request.POST.get("meta_description")
            messages.success(request, "Save seo successfully!")
            setting.save()

        elif "appearance_submit" in request.POST:
            setting.primary_color = request.POST.get("primary_color")
            messages.success(request, "Save apperance successfully!")
            setting.save()

        elif "system_submit" in request.POST:
            setting.maintenance_mode = True if request.POST.get("maintenance_mode") else False
            messages.success(request, "Save submit successfully!")
            setting.save()

        #  PAYMENT
        elif "payment_submit" in request.POST:
            setting.razorpay_key_id = request.POST.get("razorpay_key_id")
            setting.razorpay_key_secret = request.POST.get("razorpay_key_secret")
            messages.success(request, "Save payment setting successfully!")
            setting.save()
            
        return redirect("general_settings")

    return render(request, "settings_module/general_settings.html", {"setting": setting})