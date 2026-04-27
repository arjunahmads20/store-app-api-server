from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Province(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class RegencyMunicipality(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class District(models.Model):
    regency_municipality = models.ForeignKey(RegencyMunicipality, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Village(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    post_code = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Street(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class UserAddress(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, related_name='addresses')
    receiver_name = models.CharField(max_length=100)
    receiver_phone_number = models.CharField(max_length=20)
    # Link to the Geo Hierarchy
    village = models.ForeignKey(Village, on_delete=models.SET_NULL, null=True) 
    street = models.ForeignKey(Street, on_delete=models.SET_NULL, null=True) # Keep for street name master list? 
    # Or maybe street is just text? Model says FK. 
    # I'll keep as is but add Village to enable the full address retrieval.
    lattitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    other_details = models.TextField(null=True, blank=True)
    is_main_address = models.BooleanField(default=False)
    is_office = models.BooleanField(default=False)
    datetime_added = models.DateTimeField(auto_now_add=True)
    datetime_last_updated = models.DateTimeField(auto_now=True)
