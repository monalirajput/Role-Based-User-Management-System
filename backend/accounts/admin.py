from django.contrib import admin

# Register your models here.
from .models import CustomUser
from .models import MT5Account
admin.site.register(CustomUser)
from .models import MT5Account