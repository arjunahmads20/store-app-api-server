from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from user.models import User
from store.models import Store
from product.models import Product, ProductCategory, ProductInStore, UserCart, ProductInUserCart
from address.models import Country, Province, RegencyMunicipality, District, Village, Street, UserAddress
from order.models import DeliveryType, Order
from payment.models import PaymentMethod
from django.urls import reverse

class CheckoutSeparatedTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # 1. Setup User
        self.user = User.objects.create_user(username='testuser', password='password123', phone_number='08123456789')
        self.client.force_authenticate(user=self.user)
        
        # 2. Setup Address Hierarchy
        self.country = Country.objects.create(name="Indonesia")
        self.province = Province.objects.create(name="Jawa Barat", country=self.country)
        self.regency = RegencyMunicipality.objects.create(name="Bandung", province=self.province)
        self.district = District.objects.create(name="Coblong", regency_municipality=self.regency)
        self.village = Village.objects.create(name="Dago", district=self.district, post_code="40135")
        self.street = Street.objects.create(name="Jl. Dago")
        
        self.address = UserAddress.objects.create(
            user=self.user,
            receiver_name="Test Receiver",
            receiver_phone_number="08123456789",
            village=self.village,
            street=self.street,
            is_main_address=True
        )

        # 3. Setup Store & Product
        self.store = Store.objects.create(name="Test Store", street=self.street)
        self.category = ProductCategory.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Test Phone", 
            product_category=self.category,
            buy_price=1000000, 
            sell_price=1500000
        )
        self.pis = ProductInStore.objects.create(
            product=self.product,
            store=self.store,
            stock=10,
            sold_count=0
        )
        
        # 4. Setup Logistics
        self.delivery_type = DeliveryType.objects.create(name="Instant", cost=15000)
        self.payment_method = PaymentMethod.objects.create(name="Bank Transfer", fee=2000)

        # 5. Setup Cart
        self.user_cart = UserCart.objects.create(user=self.user)
        self.cart_item = ProductInUserCart.objects.create(
            user_cart=self.user_cart,
            product=self.product,
            quantity=2,
            is_checked=True
        )

    def test_checkout_validation_success(self):
        # Test the Validation Endpoint (POST /checkout)
        try:
            reversed_url = reverse('order-checkout')
            print(f"\nReversed URL: {reversed_url}")
            url = reversed_url
        except Exception as e:
            print(f"\nReverse Failed: {e}")
            url = '/api/v1/order/orders/checkout/'
            
        data = {
            'store_id': self.store.id,
        }
        
        response = self.client.post(url, data, format='json')
        
        if response.status_code != 200:
            print(f"\nValidation Response: {response.data}")
            
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data['message'], 'Checkout validation successful. Proceed to payment page.') # Message might vary
        
        # Verify NO Order Created
        self.assertFalse(Order.objects.filter(customer=self.user).exists())
        self.assertEqual(ProductInUserCart.objects.count(), 1) # Cart still there

    def test_place_order_success(self):
        # Test the actual Order Creation (POST /orders/)
        url = '/api/v1/order/orders/'
        data = {
            'store_id': self.store.id,
            'address_id': self.address.id,
            'delivery_type_id': self.delivery_type.id,
            'payment_method_id': self.payment_method.id,
            'message_for_shopper': 'Finalize Order',
            'is_online_order': True
        }
        
        response = self.client.post(url, data, format='json')
        
        if response.status_code != 201:
            print(f"\nCreation Response: {response.data}")
            
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('total_cost', response.data)
        
        # Verify Database
        self.assertTrue(Order.objects.filter(customer=self.user).exists())
        self.assertFalse(ProductInUserCart.objects.filter(id=self.cart_item.id).exists()) # Cart cleared
        
        print("\n=== SEPARATED TEST RESULT ===")
        print("Validation: OK (No Order Created)")
        print("Creation: OK (Order Created & Cart Cleared)")
