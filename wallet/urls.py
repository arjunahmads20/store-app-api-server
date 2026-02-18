from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserWalletViewSet, TopupWalletBalanceRuleViewSet, 
    UserTopupWalletBalanceViewSet, UserTransferWalletBalanceViewSet
)

router = DefaultRouter()
router.register(r'user-wallets', UserWalletViewSet, basename='userwallet')
router.register(r'topup-wallet-balance-rules', TopupWalletBalanceRuleViewSet, basename='topupwalletbalancerule')
router.register(r'user-topup-wallet-balances', UserTopupWalletBalanceViewSet, basename='usertopupwalletbalance')
router.register(r'user-transfer-wallet-balances', UserTransferWalletBalanceViewSet, basename='usertransferwalletbalance')

urlpatterns = [
    path('', include(router.urls)),
]
