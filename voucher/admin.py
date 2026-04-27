from django.contrib import admin
from .models import (
    VoucherOrder, VoucherOrderCode, UserVoucherOrder
)

admin.site.register(VoucherOrder)
admin.site.register(VoucherOrderCode)
admin.site.register(UserVoucherOrder)
