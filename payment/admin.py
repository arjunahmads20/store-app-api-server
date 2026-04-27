from django.contrib import admin
from .models import (
    PaymentMethod, UserPaymentMethod, UserTopupWalletBalancePayment, OrderPayment
)

admin.site.register(PaymentMethod)
admin.site.register(UserPaymentMethod)
admin.site.register(UserTopupWalletBalancePayment)
admin.site.register(OrderPayment)
