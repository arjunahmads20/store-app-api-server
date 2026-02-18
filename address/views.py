from rest_framework import viewsets
from .filters import (
    ProvinceFilter, RegencyMunicipalityFilter, 
    DistrictFilter, VillageFilter
)
from .models import Country, Province, RegencyMunicipality, District, Village, Street, UserAddress
from .serializers import (
    CountrySerializer, ProvinceSerializer, RegencyMunicipalitySerializer, 
    DistrictSerializer, VillageSerializer, StreetSerializer, UserAddressSerializer
)
from rest_framework.exceptions import ValidationError

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer

    filterset_class = ProvinceFilter

    def get_queryset(self):
        parent_pk = self.kwargs.get('country_pk')
        if parent_pk:
            return Province.objects.filter(country_id=parent_pk)
        return super().get_queryset()

class RegencyMunicipalityViewSet(viewsets.ModelViewSet):
    queryset = RegencyMunicipality.objects.all()
    serializer_class = RegencyMunicipalitySerializer

    filterset_class = RegencyMunicipalityFilter

    def get_queryset(self):
        parent_pk = self.kwargs.get('province_pk')
        if parent_pk:
            return RegencyMunicipality.objects.filter(province_id=parent_pk)
        return super().get_queryset()

class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

    filterset_class = DistrictFilter

    def get_queryset(self):
        parent_pk = self.kwargs.get('regency_municipality_pk')
        if parent_pk:
            return District.objects.filter(regency_municipality_id=parent_pk)
        return super().get_queryset()

class VillageViewSet(viewsets.ModelViewSet):
    queryset = Village.objects.all()
    serializer_class = VillageSerializer

    filterset_class = VillageFilter

    def get_queryset(self):
        parent_pk = self.kwargs.get('district_pk')
        if parent_pk:
            return Village.objects.filter(district_id=parent_pk)
        return super().get_queryset()

class StreetViewSet(viewsets.ModelViewSet):
    queryset = Street.objects.all()
    serializer_class = StreetSerializer

from rest_framework.permissions import IsAuthenticated
from store_api_server.permissions import IsOwner

class UserAddressViewSet(viewsets.ModelViewSet):
    """
    Manages user addresses.
    - Owners only (CRUD).
    - Enforces max one 'is_main_address'.
    - Validates Latitude/Longitude.
    """
    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def _handle_main_address(self, user, is_main):
        """
        If the new/updated address is main, set all other addresses of this user to False.
        """
        if is_main:
            UserAddress.objects.filter(user=user, is_main_address=True).update(is_main_address=False)

    def perform_create(self, serializer):
        user = self.request.user
        
        # Validation checks
        lat = serializer.validated_data.get('lattitude')
        long = serializer.validated_data.get('longitude')
        if lat and (lat < -90 or lat > 90):
             raise ValidationError("Latitude must be between -90 and 90.")
        if long and (long < -180 or long > 180):
             raise ValidationError("Longitude must be between -180 and 180.")

        self._handle_main_address(user, serializer.validated_data.get('is_main_address', False))
        serializer.save(user=user)

    def perform_update(self, serializer):
        instance = serializer.instance
        if instance.user != self.request.user:
            raise ValidationError("You do not own this address.")
            
        # Validation checks
        lat = serializer.validated_data.get('lattitude')
        long = serializer.validated_data.get('longitude')
        if lat and (lat < -90 or lat > 90):
             raise ValidationError("Latitude must be between -90 and 90.")
        if long and (long < -180 or long > 180):
             raise ValidationError("Longitude must be between -180 and 180.")

        self._handle_main_address(self.request.user, serializer.validated_data.get('is_main_address', False))
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise ValidationError("You do not own this address.")
        instance.delete()

    def get_queryset(self):
         if self.request.user.is_staff:
             return UserAddress.objects.all()
         return UserAddress.objects.filter(user=self.request.user)
