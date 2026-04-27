from rest_framework import serializers
from .models import PaymentMethod, UserPaymentMethod, UserTopupWalletBalancePayment, OrderPayment

class PaymentMethodSerializer(serializers.ModelSerializer):
    original_fee = serializers.DecimalField(source='fee', max_digits=12, decimal_places=2, read_only=True)
    discounted_fee = serializers.SerializerMethodField()

    class Meta:
        model = PaymentMethod
        exclude = ['datetime_added', 'datetime_last_updated']

    def get_discounted_fee(self, obj):
        return obj.fee - obj.discount

class UserPaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPaymentMethod
        fields = '__all__'

class UserTopupWalletBalancePaymentSerializer(serializers.ModelSerializer):
    payment_method = PaymentMethodSerializer(read_only=True)

    class Meta:
        model = UserTopupWalletBalancePayment
        fields = '__all__'

from voucher.serializers import UserVoucherOrderSerializer

class OrderPaymentSerializer(serializers.ModelSerializer):
    payment_method = PaymentMethodSerializer(read_only=True)
    user_voucher_order = UserVoucherOrderSerializer(read_only=True)
    
    class Meta:
        model = OrderPayment
        fields = '__all__'
