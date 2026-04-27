from django.db import models

class NetflixDiscountPointReedem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    point_required = models.PositiveIntegerField()
    min_membership = models.ForeignKey('membership.Membership', on_delete=models.CASCADE, null=True, blank=True)
    netflix_discount_id = models.CharField(max_length=100) # External ID
    min_movie_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_precentage = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    max_nominal_discount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    datetime_started = models.DateTimeField(auto_now_add=True) # Assuming started when added/created

class UserNetflixDiscountPointReedem(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    netflix_discount_reedem = models.ForeignKey(NetflixDiscountPointReedem, on_delete=models.CASCADE)
    datetime_added = models.DateTimeField(auto_now_add=True)
    datetime_reedem = models.DateTimeField(null=True, blank=True)

class VoucherOrderPointReedem(models.Model):
    voucher_order = models.OneToOneField('voucher.VoucherOrder', on_delete=models.CASCADE)
    point_required = models.PositiveIntegerField()
    min_membership = models.ForeignKey('membership.Membership', on_delete=models.CASCADE, null=True, blank=True)
    datetime_started = models.DateTimeField(auto_now_add=True)
