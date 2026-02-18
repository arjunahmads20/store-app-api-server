from rest_framework import serializers
from .models import Order, ProductInOrder, DeliveryType, OrderReview, ProductInOrderReview

class DeliveryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryType
        fields = '__all__'

from product.serializers import ProductSerializer

class ProductInOrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    # High-level attributes
    flashsale_discount_percentage = serializers.SerializerMethodField()
    product_discount_percentage = serializers.SerializerMethodField()
    point_earned = serializers.SerializerMethodField()

    class Meta:
        model = ProductInOrder
        fields = '__all__'

    def get_flashsale_discount_percentage(self, obj):
        if obj.product_in_store_in_flashsale:
            return obj.product_in_store_in_flashsale.discount_precentage
        return 0

    def get_product_discount_percentage(self, obj):
        if obj.product_in_store_in_product_in_store_discount:
            # Need to traverse to the actual discount definition
            return obj.product_in_store_in_product_in_store_discount.product_in_store_discount.discount_precentage
        return 0

    def get_point_earned(self, obj):
        if obj.product_in_store_point:
            return obj.product_in_store_point.point_earned
        return 0

class OrderSerializer(serializers.ModelSerializer):
    delivery_type = DeliveryTypeSerializer(read_only=True)
    products = ProductInOrderSerializer(many=True, read_only=True)
    # Payment info via MethodField
    payment_info = serializers.SerializerMethodField()
    # Costs
    total_product_cost = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()
    point_earned_total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_payment_info(self, obj):
        from payment.models import OrderPayment
        from payment.serializers import OrderPaymentSerializer
        payment = OrderPayment.objects.filter(order=obj).select_related('payment_method', 'user_voucher_order__voucher_order').first()
        if payment:
            # We construct a custom dict to satisfy "order_payment instance and the payment_method instance"
            # and "user_voucher_order and voucher_order" requirements cleanly.
            return OrderPaymentSerializer(payment).data
        return None

    def get_point_earned_total(self, obj):
        total_points = 0
        for pio in obj.products.all():
            if pio.product_in_store_point:
                total_points += pio.product_in_store_point.point_earned * pio.quantity
        return total_points

    def calculate_product_cost(self, obj):
        # 1. Product Costs
        total_product_cost = 0
        products = obj.products.select_related(
            'product', 
            'product_in_store_in_flashsale', 
            'product_in_store_in_product_in_store_discount__product_in_store_discount'
        )
        for pio in products:
            price = pio.product.sell_price 
            
            # Check Flashsale Discount
            if pio.product_in_store_in_flashsale:
                # Formula: Price * (1 - discount/100)
                disc = pio.product_in_store_in_flashsale.discount_precentage
                price = price * (1 - disc/100)
            
            # Check Standard Discount 
            elif pio.product_in_store_in_product_in_store_discount:
                 disc = pio.product_in_store_in_product_in_store_discount.product_in_store_discount.discount_precentage
                 price = price * (1 - disc/100)
            
            total_product_cost += price * pio.quantity
        return total_product_cost

    def get_total_product_cost(self, obj):
        return round(self.calculate_product_cost(obj), 2)

    def get_total_cost(self, obj):
        total_product_cost = self.calculate_product_cost(obj)

        # 2. Delivery Cost
        delivery_cost = 0
        if obj.delivery_type:
            delivery_cost = obj.delivery_type.cost - obj.delivery_type.discount
            if delivery_cost < 0: delivery_cost = 0
            
        subtotal = total_product_cost + delivery_cost

        # 3. Voucher Discount & Payment Fee
        voucher_discount = 0
        payment_fee = 0
        
        from payment.models import OrderPayment
        payment = OrderPayment.objects.filter(order=obj).select_related('payment_method', 'user_voucher_order__voucher_order').first()
        
        if payment:
            # Payment Fee
            if payment.payment_method:
                 payment_fee = payment.payment_method.fee
            
            # Voucher Discount
            if payment.user_voucher_order:
                voucher = payment.user_voucher_order.voucher_order
                if voucher.discount_precentage > 0:
                    # Discount applies to product cost
                    disc_amount = total_product_cost * (voucher.discount_precentage / 100)
                    if voucher.max_nominal_discount and disc_amount > voucher.max_nominal_discount:
                        disc_amount = voucher.max_nominal_discount
                    voucher_discount = disc_amount
        
        grand_total = subtotal + payment_fee - voucher_discount
        return round(grand_total, 2)

class OrderReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderReview
        fields = '__all__'

class ProductInOrderReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInOrderReview
        fields = '__all__'
