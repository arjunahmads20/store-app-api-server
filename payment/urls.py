from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PaymentMethodViewSet, UserPaymentMethodViewSet,
    UserTopupWalletBalancePaymentViewSet, OrderPaymentViewSet
)

router = DefaultRouter()
router.register(r'payment-methods', PaymentMethodViewSet, basename='paymentmethod')
router.register(r'user-payment-methods', UserPaymentMethodViewSet, basename='userpaymentmethod')
router.register(r'user-topup-wallet-balance-payments', UserTopupWalletBalancePaymentViewSet, basename='usertopupwalletbalancepayment')
router.register(r'order-payments', OrderPaymentViewSet, basename='orderpayment')

urlpatterns = [
    path('', include(router.urls)),
]
