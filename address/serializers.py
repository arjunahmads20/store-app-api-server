from rest_framework import serializers
from .models import Country, Province, RegencyMunicipality, District, Village, Street, UserAddress

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'

class RegencyMunicipalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = RegencyMunicipality
        fields = '__all__'

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = '__all__'

class StreetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Street
        fields = '__all__'

class UserAddressSerializer(serializers.ModelSerializer):
    # Nested Serialization for Read
    village_detail = VillageSerializer(source='village', read_only=True)
    district_detail = DistrictSerializer(source='village.district', read_only=True)
    regency_detail = RegencyMunicipalitySerializer(source='village.district.regency_municipality', read_only=True)
    province_detail = ProvinceSerializer(source='village.district.regency_municipality.province', read_only=True)
    country_detail = CountrySerializer(source='village.district.regency_municipality.province.country', read_only=True)
    street_detail = StreetSerializer(source='street', read_only=True)

    # Write Fields
    village = serializers.PrimaryKeyRelatedField(queryset=Village.objects.all())
    street = serializers.PrimaryKeyRelatedField(queryset=Street.objects.all())

    class Meta:
        model = UserAddress
        fields = [
            'id', 'user', 'receiver_name', 'receiver_phone_number',
            'village', 'street', 
            'village_detail', 'district_detail', 'regency_detail', 'province_detail', 'country_detail', 'street_detail',
            'lattitude', 'longitude', 'other_details', 'is_main_address', 'is_office',
            'datetime_added', 'datetime_last_updated'
        ]
        read_only_fields = ['user', 'datetime_added', 'datetime_last_updated']

    def create(self, validated_data):
        # Auto-assign user
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
