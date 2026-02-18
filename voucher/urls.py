from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VoucherOrderViewSet, VoucherOrderCodeViewSet, UserVoucherOrderViewSet

router = DefaultRouter()
router.register(r'voucher-orders', VoucherOrderViewSet, basename='voucherorder')
router.register(r'voucher-order-codes', VoucherOrderCodeViewSet, basename='voucherordercode')
router.register(r'user-voucher-orders', UserVoucherOrderViewSet, basename='uservoucherorder')

urlpatterns = [
    path('', include(router.urls)),
]
