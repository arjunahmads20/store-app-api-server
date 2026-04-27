from django.contrib import admin
from .models import (
    UserWallet, TopupWalletBalanceRule, UserTopupWalletBalance,
    UserTransferWalletBalance
)

admin.site.register(UserWallet)
admin.site.register(TopupWalletBalanceRule)
admin.site.register(UserTopupWalletBalance)
admin.site.register(UserTransferWalletBalance)
