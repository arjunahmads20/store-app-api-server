from rest_framework import serializers
from .models import UserWallet, TopupWalletBalanceRule, UserTopupWalletBalance, UserTransferWalletBalance

class UserWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWallet
        fields = '__all__'

class TopupWalletBalanceRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopupWalletBalanceRule
        fields = '__all__'

class UserTopupWalletBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTopupWalletBalance
        fields = '__all__'

class UserTransferWalletBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTransferWalletBalance
        fields = '__all__'
