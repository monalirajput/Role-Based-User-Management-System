from django.db import models

class SiteSetting(models.Model):
    site_name = models.CharField(max_length=200, default="My Website" )
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    timezone = models.CharField(max_length=100, blank=True)

    # SEO
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)

    # Appearance
    primary_color = models.CharField(max_length=20, blank=True)

    # System
    maintenance_mode = models.BooleanField(default=False)
    
     #(Payment Settings)
    razorpay_key_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_key_secret = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.site_name
