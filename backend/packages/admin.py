from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Package

admin.site.register(Package)