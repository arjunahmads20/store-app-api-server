from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from user.models import User
from store.models import Store
from product.models import Product, ProductCategory, ProductInStore, UserCart, ProductInUserCart
from address.models import Street
from voucher.models import VoucherOrder, UserVoucherOrder

class VoucherLogicTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password123', daily_product_quota=100)
        self.client.force_authenticate(user=self.user)
        
        self.street = Street.objects.create(name="Jl. Dago")
        self.store = Store.objects.create(name="Test Store", street=self.street)
        self.category = ProductCategory.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Test Phone", 
            product_category=self.category,
            buy_price=1000000, 
            sell_price=1500000 # 1.5M
        )
        self.pis = ProductInStore.objects.create(
            product=self.product,
            store=self.store,
            stock=100,
            sold_count=0
        )
        # Cart item: 1 item @ 1.5M
        self.user_cart = UserCart.objects.create(user=self.user)
        self.cart_item = ProductInUserCart.objects.create(
            user_cart=self.user_cart,
            product=self.product,
            quantity=1,
            is_checked=True
        )

        # Base Voucher
        self.voucher = VoucherOrder.objects.create(
            name="Discount", 
            source_type='code',
            min_item_quantity=2, # Requires 2 items
            min_item_cost=2000000, # Requires 2M
            datetime_started=timezone.now() - timedelta(days=1),
            datetime_expiry=timezone.now() + timedelta(days=1)
        )
        self.user_voucher = UserVoucherOrder.objects.create(user=self.user, voucher_order=self.voucher)
        
        self.checkout_url = '/api/v1/order/orders/checkout/'

    def test_min_qty_fail(self):
        # Cart has 1 item, voucher needs 2
        data = {'store_id': self.store.id, 'user_voucher_order_id': self.user_voucher.id}
        response = self.client.post(self.checkout_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Minimum item quantity', str(response.data))

    def test_min_cost_fail(self):
        # Update qty to 2, cost = 3M. Satisfies qty(2) and cost(2M).
        # Wait, let's test fail first.
        # Make voucher require 5M
        self.voucher.min_item_cost = 5000000
        self.voucher.save()
        
        self.cart_item.quantity = 2
        self.cart_item.save() # Cost 3M
        
        data = {'store_id': self.store.id, 'user_voucher_order_id': self.user_voucher.id}
        response = self.client.post(self.checkout_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Minimum purchase', str(response.data))

    def test_success_application(self):
        # Make requirements met
        self.voucher.min_item_cost = 1000000
        self.voucher.save()
        self.cart_item.quantity = 2
        self.cart_item.save()
        
        data = {'store_id': self.store.id, 'user_voucher_order_id': self.user_voucher.id}
        response = self.client.post(self.checkout_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_expired_voucher(self):
        self.voucher.datetime_expiry = timezone.now() - timedelta(days=1)
        self.voucher.save()
        
        data = {'store_id': self.store.id, 'user_voucher_order_id': self.user_voucher.id}
        response = self.client.post(self.checkout_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('expired', str(response.data))
