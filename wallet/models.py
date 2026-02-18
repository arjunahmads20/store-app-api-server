from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator

class UserWallet(models.Model):
    user = models.OneToOneField('user.User', on_delete=models.CASCADE, related_name='wallet')
    account_number = models.CharField(max_length=50, unique=True)
    pin_number = models.CharField(
        max_length=6, 
        validators=[RegexValidator(r'^\d{6}$', 'PIN must be exactly 6 digits.')],
        blank=True, 
        null=True
    )
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username}'s Wallet"

class TopupWalletBalanceRule(models.Model):
    min_nominal_topup = models.DecimalField(max_digits=12, decimal_places=2)
    max_nominal_topup = models.DecimalField(max_digits=12, decimal_places=2)
    point_earned = models.IntegerField(default=0)
    datetime_added = models.DateTimeField(auto_now_add=True)
    datetime_last_updated = models.DateTimeField(auto_now=True)
    datetime_started = models.DateTimeField(null=True, blank=True)
    datetime_finished = models.DateTimeField(null=True, blank=True)

class UserTopupWalletBalance(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    wallet = models.ForeignKey(UserWallet, on_delete=models.CASCADE)
    nominal_topup = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')
    point_earned = models.IntegerField(default=0)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_finished = models.DateTimeField(null=True, blank=True)

class UserTransferWalletBalance(models.Model):
    sender = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='transfers_sent')
    receiver = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='transfers_received')
    nominal_transfer = models.DecimalField(max_digits=12, decimal_places=2)
    admin_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_finished = models.DateTimeField(null=True, blank=True)
