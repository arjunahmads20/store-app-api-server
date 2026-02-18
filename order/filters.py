import django_filters
from .models import Order, ProductInOrderReview, OrderReview

class OrderFilter(django_filters.FilterSet):
    payment_method = django_filters.NumberFilter(field_name='orderpayment__payment_method__id')
    payment_method_name = django_filters.CharFilter(field_name='orderpayment__payment_method__name', lookup_expr='icontains')
    
    # Existing filters from view
    status = django_filters.CharFilter(field_name='status')
    store = django_filters.NumberFilter(field_name='store')
    delivery_type = django_filters.NumberFilter(field_name='delivery_type')

    class Meta:
        model = Order
        fields = ['status', 'store', 'delivery_type', 'payment_method', 'payment_method_name']

class OrderReviewFilter(django_filters.FilterSet):
    order = django_filters.NumberFilter(field_name="order__id")

    class Meta:
        model = OrderReview
        fields = ['order']

class ProductInOrderReviewFilter(django_filters.FilterSet):
    product = django_filters.NumberFilter(field_name="product_in_order__product__id")

    class Meta:
        model = ProductInOrderReview
        fields = ['product', 'product_in_order']
