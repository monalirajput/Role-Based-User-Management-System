from django.urls import path
from .views import subscription_expired
from . import views
urlpatterns = [
    path('expired/', subscription_expired, name='subscription_expired'),
    path("create-order/", views.create_order, name="create_order"),
    path("verify-payment/", views.verify_payment, name="verify_payment"),
    path('transactions/', views.transactions_view, name='transactions'),
]