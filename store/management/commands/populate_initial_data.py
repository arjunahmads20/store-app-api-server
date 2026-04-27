from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from user.models import User
from store.models import Store
from product.models import (
    ProductCategory, Product, ProductInStore, 
    ProductInStoreDiscount, ProductInStoreInProductInStoreDiscount,
    Flashsale, ProductInStoreInFlashsale, UserCart, ProductInUserCart
)
from address.models import Country, Province, RegencyMunicipality, District, Village, Street
from order.models import DeliveryType
from payment.models import PaymentMethod

class Command(BaseCommand):
    help = 'Populates initial data for the store'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating data...')

        # 1. Location Data (Indonesia Sample)
        country, _ = Country.objects.get_or_create(name='Indonesia')
        province, _ = Province.objects.get_or_create(name='DKI Jakarta', country=country)
        regency, _ = RegencyMunicipality.objects.get_or_create(name='Jakarta Selatan', province=province)
        district, _ = District.objects.get_or_create(name='Kebayoran Baru', regency_municipality=regency)
        village, _ = Village.objects.get_or_create(name='Senayan', district=district, post_code='12190')
        street, _ = Street.objects.get_or_create(name='Jl. Jend. Sudirman')

        self.stdout.write(self.style.SUCCESS(f'Locations created.'))

        # 2. Store
        store, _ = Store.objects.get_or_create(
            name='Store Cabang Senayan',
            defaults={
                'street': street,
                'lattitude': Decimal('-6.229746'),
                'longitude': Decimal('106.816430'),
            }
        )
        self.stdout.write(self.style.SUCCESS(f'Store created: {store.name}'))

        # 3. Delivery Types
        # • Instant, cost: Rp5.000
        # • 07.00 - 07.59, cost: free (Model doesn't support time slots yet, just adding names for now)
        DeliveryType.objects.get_or_create(name='Instant Delivery', defaults={'cost': 5000})
        DeliveryType.objects.get_or_create(name='07.00 - 07.59 Delivery', defaults={'cost': 0})
        DeliveryType.objects.get_or_create(name='08.00 - 08.59 Delivery', defaults={'cost': 10000}) # Assumption
        
        self.stdout.write(self.style.SUCCESS(f'Delivery types created.'))

        # 4. Payment Methods
        PaymentMethod.objects.get_or_create(
            name='Cash on Delivery (COD)',
            defaults={'fee': 500, 'discount': 0}
        )
        self.stdout.write(self.style.SUCCESS(f'Payment methods created.'))

        # 5. Product Categories
        cat_food, _ = ProductCategory.objects.get_or_create(name='Fresh Food', defaults={'icon_url': 'http://example.com/food.png'})
        cat_beverage, _ = ProductCategory.objects.get_or_create(name='Beverages', defaults={'icon_url': 'http://example.com/drink.png'})

        # 6. Products
        # Apple
        p_apple, _ = Product.objects.get_or_create(
            name='Fuji Apple',
            defaults={
                'product_category': cat_food,
                'buy_price': 5000,
                'sell_price': 8000,
                'unit': 'kg',
                'size': 1,
                'is_support_instant_delivery': True
            }
        )
        # Milk
        p_milk, _ = Product.objects.get_or_create(
            name='Fresh Milk 1L',
            defaults={
                'product_category': cat_beverage,
                'buy_price': 15000,
                'sell_price': 18000,
                'unit': 'bottle',
                'size': 1,
                'is_support_instant_delivery': True
            }
        )

        # 7. Inventory (ProductInStore)
        pis_apple, _ = ProductInStore.objects.get_or_create(
            product=p_apple,
            store=store,
            defaults={'stock': 100}
        )
        pis_milk, _ = ProductInStore.objects.get_or_create(
            product=p_milk,
            store=store,
            defaults={'stock': 50}
        )

        # 8. Discounts
        # 10% off Apple
        discount_obj, _ = ProductInStoreDiscount.objects.get_or_create(
            discount_label='Fresh Promo',
            defaults={'discount_precentage': 10}
        )
        ProductInStoreInProductInStoreDiscount.objects.get_or_create(
            product_in_store=pis_apple,
            product_in_store_discount=discount_obj,
            defaults={
                'datetime_started': timezone.now(),
                'datetime_ended': timezone.now() + timedelta(days=7)
            }
        )

        # 9. Flashsale
        fs, _ = Flashsale.objects.get_or_create(
            name='Morning Flashsale',
            defaults={
                'datetime_started': timezone.now(),
                'datetime_ended': timezone.now() + timedelta(hours=2)
            }
        )
        ProductInStoreInFlashsale.objects.get_or_create(
            product_in_store=pis_milk,
            flashsale=fs,
            defaults={
                'discount_precentage': 20,
                'stock': 10,
                'quantity_limit': 2
            }
        )

        # 10. User
        user, created = User.objects.get_or_create(username='customer1', email='customer1@example.com')
        if created:
            user.set_password('password123')
            user.save()
        
        # 11. User Cart
        cart, _ = UserCart.objects.get_or_create(user=user)
        ProductInUserCart.objects.get_or_create(
            product=p_apple,
            user_cart=cart,
            defaults={'quantity': 2}
        )

        self.stdout.write(self.style.SUCCESS(f'Data population completed successfully.'))
