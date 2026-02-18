from rest_framework import serializers
from .models import VoucherOrder, VoucherOrderCode, UserVoucherOrder

class VoucherOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoucherOrder
        fields = '__all__'

class VoucherOrderCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoucherOrderCode
        fields = '__all__'

class UserVoucherOrderSerializer(serializers.ModelSerializer):
    voucher_order = VoucherOrderSerializer(read_only=True)

    class Meta:
        model = UserVoucherOrder
        fields = '__all__'
