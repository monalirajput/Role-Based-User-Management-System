from django.contrib import admin
from django.urls import path, include
from accounts.views import user_login
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('subscriptions/', include('subscriptions.urls')),
    # Home page
    path('', user_login, name='home'),

    # Apps
    path('accounts/', include('accounts.urls')),
    path('settings/', include('settings_module.urls')),
    path('packages/', include('packages.urls')),
    
    

    # Password Change
    path('password-change/', 
         auth_views.PasswordChangeView.as_view(
             template_name='accounts/change_password.html'
         ),
         name='password_change'),

    path('password-change-done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='accounts/change_password_done.html'
         ),
         name='password_change_done'),
]

# Media Files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)