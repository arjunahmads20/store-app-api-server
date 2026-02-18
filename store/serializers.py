from rest_framework import serializers
from .models import Store

class StoreSerializer(serializers.ModelSerializer):
    street_name = serializers.CharField(source='street.name', read_only=True)
    village_name = serializers.CharField(source='village.name', read_only=True)
    district_name = serializers.CharField(source='village.district.name', read_only=True)

    class Meta:
        model = Store
        fields = '__all__'
