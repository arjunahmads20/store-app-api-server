from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NetflixDiscountPointReedemViewSet, UserNetflixDiscountPointReedemViewSet, VoucherOrderPointReedemViewSet
)

router = DefaultRouter()
router.register(r'netflix-discount-point-reedems', NetflixDiscountPointReedemViewSet, basename='netflixdiscountpointreedem')
router.register(r'user-netflix-discount-point-reedems', UserNetflixDiscountPointReedemViewSet, basename='usernetflixdiscountpointreedem')
router.register(r'voucher-order-point-reedems', VoucherOrderPointReedemViewSet, basename='voucherorderpointreedem')

urlpatterns = [
    path('', include(router.urls)),
]
