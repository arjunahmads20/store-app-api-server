from rest_framework import serializers
from .models import NetflixDiscountPointReedem, UserNetflixDiscountPointReedem, VoucherOrderPointReedem

class NetflixDiscountPointReedemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetflixDiscountPointReedem
        fields = '__all__'

class UserNetflixDiscountPointReedemSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNetflixDiscountPointReedem
        fields = '__all__'

class VoucherOrderPointReedemSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoucherOrderPointReedem
        fields = '__all__'
