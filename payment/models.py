from django.db import models

class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)
    fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    datetime_added = models.DateTimeField(auto_now_add=True)
    datetime_last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class UserPaymentMethod(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=50)
    token = models.CharField(max_length=255, null=True, blank=True)
    datetime_added = models.DateTimeField(auto_now_add=True)

class UserTopupWalletBalancePayment(models.Model):
    topup_wallet_balance = models.ForeignKey('wallet.UserTopupWalletBalance', on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=50) # Optional if using midtrans
    transaction_token = models.CharField(max_length=255, null=True, blank=True)
    transaction_redirect_url = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_finished = models.DateTimeField(null=True, blank=True)

class OrderPayment(models.Model):
    order = models.ForeignKey('order.Order', on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    account_number = models.CharField(max_length=50) # Optional if using midtrans
    transaction_token = models.CharField(max_length=255, null=True, blank=True)
    transaction_redirect_url = models.CharField(max_length=255, null=True, blank=True)
    user_voucher_order = models.ForeignKey('voucher.UserVoucherOrder', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_finished = models.DateTimeField(null=True, blank=True)




#SAMPLE REQUEST START HERE

import midtransclient
# Create Snap API instance
snap = midtransclient.Snap(
    # Set to true if you want Production Environment (accept real transaction).
    is_production=False,
    server_key='Mid-server-aIk7THaQ4T0Hg8DDLu7J5-9f'
)

from django.db.models.signals import post_save
from django.dispatch import receiver
from order.serializers import OrderSerializer

@receiver(post_save, sender=OrderPayment)
def order_payment_post_save(sender, instance, created, **kwargs):
    if created and instance.payment_method.name != 'COD':

        payment_id = instance.id
        order_id = instance.order.id
        total_cost = float(OrderSerializer(instance.order).data['total_cost'])
        customer_first_name = instance.order.customer.first_name
        customer_last_name = instance.order.customer.last_name
        customer_email = instance.order.customer.email
        customer_phone = instance.order.customer.phone_number

        # Build API parameter
        params = {
            "transaction_details": {
                "order_id": order_id,
                "gross_amount": total_cost
            }, "customer_details":{
                "first_name": customer_first_name,
                "last_name": customer_last_name,
                "email": customer_email,
                "phone": customer_phone
            }
        }

        transaction = snap.create_transaction(params)

        instance.transaction_token = transaction['token']
        instance.transaction_redirect_url = transaction['redirect_url']
        instance.save()

        