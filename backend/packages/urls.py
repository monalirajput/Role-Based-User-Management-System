from django.urls import path
from . import views

urlpatterns = [
    path('', views.package_list, name='package_list'),
    path('add/', views.package_create, name='package_add'),
    path('edit/<int:pk>/', views.package_update, name='package_edit'),
    path('delete/<int:pk>/', views.package_delete, name='package_delete'),
]