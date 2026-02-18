from django.urls import path, include
from rest_framework_nested import routers
from .views import (
    CountryViewSet, ProvinceViewSet, RegencyMunicipalityViewSet, 
    DistrictViewSet, VillageViewSet, StreetViewSet, UserAddressViewSet
)

# Main
router = routers.SimpleRouter()
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'streets', StreetViewSet, basename='street')
router.register(r'user-addresses', UserAddressViewSet, basename='useraddress')
# Note: Keeping sub-resources compatible with top-level access if needed? 
# Usually deep hierarchy forces top-down. 
# But for admin, maybe top level needed. 
router.register(r'provinces', ProvinceViewSet, basename='province') 
router.register(r'regency-municipalities', RegencyMunicipalityViewSet, basename='regencymunicipality')
router.register(r'districts', DistrictViewSet, basename='district')
router.register(r'villages', VillageViewSet, basename='village')


# Nested
# Country -> Province
countries_router = routers.NestedSimpleRouter(router, r'countries', lookup='country')
countries_router.register(r'provinces', ProvinceViewSet, basename='country-province')

# Province -> Regency
provinces_router = routers.NestedSimpleRouter(countries_router, r'provinces', lookup='province')
provinces_router.register(r'regency-municipalities', RegencyMunicipalityViewSet, basename='province-regencymunicipality')

# Regency -> District
regencies_router = routers.NestedSimpleRouter(provinces_router, r'regency-municipalities', lookup='regency_municipality')
regencies_router.register(r'districts', DistrictViewSet, basename='regencymunicipality-district')

# District -> Village
districts_router = routers.NestedSimpleRouter(regencies_router, r'districts', lookup='district')
districts_router.register(r'villages', VillageViewSet, basename='district-village')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(countries_router.urls)),
    path('', include(provinces_router.urls)),
    path('', include(regencies_router.urls)),
    path('', include(districts_router.urls)),
]
