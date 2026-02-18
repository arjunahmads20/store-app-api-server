from django.contrib import admin
from .models import (
    Country, Province, RegencyMunicipality, District, Village, Street, UserAddress
)

admin.site.register(Country)
admin.site.register(Province)
admin.site.register(RegencyMunicipality)
admin.site.register(District)
admin.site.register(Village)
admin.site.register(Street)
admin.site.register(UserAddress)
