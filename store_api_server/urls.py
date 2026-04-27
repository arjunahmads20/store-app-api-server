from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/', include('user.urls')),
    path('api/v1/address/', include('address.urls')),
    path('api/v1/wallet/', include('wallet.urls')),
    path('api/v1/membership/', include('membership.urls')),
    path('api/v1/product/', include('product.urls')),
    path('api/v1/order/', include('order.urls')),
    path('api/v1/payment/', include('payment.urls')),
    path('api/v1/voucher/', include('voucher.urls')),
    path('api/v1/point/', include('point.urls')),
    path('api/v1/store/', include('store.urls')),
]
