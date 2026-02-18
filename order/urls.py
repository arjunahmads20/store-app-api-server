from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import (
    OrderViewSet, ProductInOrderViewSet, DeliveryTypeViewSet,
    OrderReviewViewSet, ProductInOrderReviewViewSet
)

# Main
router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'delivery-types', DeliveryTypeViewSet, basename='deliverytype')
router.register(r'product-in-order-reviews', ProductInOrderReviewViewSet, basename='productinorderreview') 

router.register(r'order-reviews', OrderReviewViewSet, basename='orderreview')

# Note: Deep nesting (orders -> items -> reviews) is possible but keeping it simple for items-reviews unless requested.
# The user asked for /orders/2/products.

# Nested Orders
orders_router = routers.NestedSimpleRouter(router, r'orders', lookup='order')
orders_router.register(r'product-in-orders', ProductInOrderViewSet, basename='order-productinorder')
orders_router.register(r'order-reviews', OrderReviewViewSet, basename='order-orderreview')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(orders_router.urls)),
]
