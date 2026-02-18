from django.db import models

class VoucherOrder(models.Model):
    SOURCE_TYPE_CHOICES = (
        ('code', 'Code'),
        ('offer', 'Offer'),
        ('membership_reward', 'Membership Reward'),
        ('point_reedem', 'Point Reddmem'),
    )
    
    name = models.CharField(max_length=255)
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPE_CHOICES)
    description = models.TextField(null=True, blank=True)
    img_url = models.URLField(max_length=500, null=True, blank=True)
    min_item_quantity = models.PositiveIntegerField(default=0)
    min_item_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_precentage = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    max_nominal_discount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    datetime_added = models.DateTimeField(auto_now_add=True)
    datetime_last_updated = models.DateTimeField(auto_now=True)
    datetime_started = models.DateTimeField(null=True, blank=True)
    datetime_expiry = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class VoucherOrderCode(models.Model):
    voucher_order = models.OneToOneField(VoucherOrder, on_delete=models.CASCADE)
    code = models.CharField(max_length=50, unique=True)
    datetime_started = models.DateTimeField(null=True, blank=True)
    datetime_ended = models.DateTimeField(null=True, blank=True)

class UserVoucherOrder(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    voucher_order = models.ForeignKey(VoucherOrder, on_delete=models.CASCADE)
    is_used = models.BooleanField(default=False)
    datetime_added = models.DateTimeField(auto_now_add=True)
