from django.contrib import admin
from .models import (
    DeliveryType, Order, ProductInOrder, OrderReview, ProductInOrderReview
)

admin.site.register(DeliveryType)
admin.site.register(Order)
admin.site.register(ProductInOrder)
admin.site.register(OrderReview)
admin.site.register(ProductInOrderReview)
