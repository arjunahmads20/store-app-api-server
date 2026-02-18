import django_filters
from .models import UserAddress, Country, Province, RegencyMunicipality, District, Village, Street

class ProvinceFilter(django_filters.FilterSet):
    country = django_filters.NumberFilter(field_name='country__id')

class RegencyMunicipalityFilter(django_filters.FilterSet):
    country = django_filters.NumberFilter(field_name='country__id')
    province = django_filters.NumberFilter(field_name='province__id')

class DistrictFilter(django_filters.FilterSet):
    country = django_filters.NumberFilter(field_name='country__id')
    province = django_filters.NumberFilter(field_name='province__id')
    regency_municipality = django_filters.NumberFilter(field_name='regency_municipality__id')

class VillageFilter(django_filters.FilterSet):
    country = django_filters.NumberFilter(field_name='country__id')
    province = django_filters.NumberFilter(field_name='province__id')
    regency_municipality = django_filters.NumberFilter(field_name='regency_municipality__id')
    district = django_filters.NumberFilter(field_name='district__id')
