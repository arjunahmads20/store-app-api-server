from django.contrib import admin
from .models import (
    NetflixDiscountPointReedem, UserNetflixDiscountPointReedem,
    VoucherOrderPointReedem
)

admin.site.register(NetflixDiscountPointReedem)
admin.site.register(UserNetflixDiscountPointReedem)
admin.site.register(VoucherOrderPointReedem)
