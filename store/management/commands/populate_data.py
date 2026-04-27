from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
import random
import string
from datetime import timedelta

# Model Imports
from store.models import Store
from product.models import (
    ProductCategory, Product, ProductInStore, UserProductFavorite,
    ProductInStorePoint, ProductInStoreDiscount,
    ProductInStoreInProductInStoreDiscount, Flashsale,
    ProductInStoreInFlashsale, UserCart, ProductInUserCart,
    StoreCart, ProductInStoreCart
)
from order.models import (
    DeliveryType, Order, ProductInOrder, OrderReview, ProductInOrderReview
)
from address.models import (
    Country, Province, RegencyMunicipality, District, Village,
    Street, UserAddress
)
from wallet.models import (
    UserWallet, TopupWalletBalanceRule, UserTopupWalletBalance,
    UserTransferWalletBalance
)
from membership.models import (
    Membership, UserMembership, UserMembershipHistory,
    PointMembershipReward, UserPointMembershipReward,
    VoucherOrderMembershipReward
)
from payment.models import (
    PaymentMethod, UserPaymentMethod, UserTopupWalletBalancePayment,
    OrderPayment
)
from voucher.models import (
    VoucherOrder, VoucherOrderCode, UserVoucherOrder
)
from point.models import (
    NetflixDiscountPointReedem, UserNetflixDiscountPointReedem,
    VoucherOrderPointReedem
)

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the database with comprehensive sample data for ALL models'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting comprehensive data population...')
        
        # Utilities
        def random_string(length=10):
            return ''.join(random.choices(string.ascii_letters, k=length))
        
        def random_digits(length=10):
            return ''.join(random.choices(string.digits, k=length))

        now = timezone.now()
        past = now - timedelta(days=30)
        future = now + timedelta(days=30)

        # 1. Users
        self.stdout.write('1. Creating Users...')
        users = []
        for i in range(15): # Increased to 15
            username = f'user_detailed_{i+1}'
            email = f'user{i+1}@example.com'
            user = User.objects.filter(username=username).first()
            if not user:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='password123',
                    phone_number=f'08{random_digits(10)}'
                )
            users.append(user)
            
            # UserWallet (OneToOne)
            # Check if wallet exists (signals might create it, or not)
            if not getattr(user, 'wallet', None):
                UserWallet.objects.create(
                    user=user,
                    account_number=f'WALLET-{user.id}-{random_digits(4)}',
                    balance=Decimal(random.randint(100000, 10000000))
                )

        # Admin
        admin_user = User.objects.filter(username='admin_master').first()
        if not admin_user:
            admin_user = User.objects.create_superuser(
                username='admin_master',
                email='admin@example.com',
                password='admin123'
            )

        # 2. Address Hierarchy
        self.stdout.write('2. Creating Address Hierarchy...')
        country, _ = Country.objects.get_or_create(name='Indonesia')
        province, _ = Province.objects.get_or_create(name='Jawa Barat', country=country)
        regency, _ = RegencyMunicipality.objects.get_or_create(name='Kota Bandung', province=province)
        district, _ = District.objects.get_or_create(name='Coblong', regency_municipality=regency)
        village, _ = Village.objects.get_or_create(name='Dago', district=district, post_code='40135')
        street, _ = Street.objects.get_or_create(name='Jl. Ir. H. Juanda')
        
        # User Addresses
        for user in users:
            UserAddress.objects.get_or_create(
                user=user,
                defaults={
                    'receiver_name': f"{user.username} Receiver",
                    'receiver_phone_number': user.phone_number or '08123456789',
                    'village': village,
                    'street': street,
                    'lattitude': Decimal('-6.890000'),
                    'longitude': Decimal('107.610000'),
                    'other_details': f'Near landmark {random_string(5)}',
                    'is_main_address': True,
                    'is_office': random.choice([True, False])
                }
            )

        # 3. Store
        self.stdout.write('3. Creating Store...')
        store, _ = Store.objects.get_or_create(
            name='Grand Store Bandung',
            defaults={
                'street': street,
                'village': village,
                'lattitude': Decimal('-6.890000'),
                'longitude': Decimal('107.610000')
            }
        )
        
        # Update ALL stores to ensure they have a village (for the API requirement)
        for s in Store.objects.filter(village__isnull=True):
            s.village = village
            s.save()
            self.stdout.write(f'Updated store {s.name} with village')

        # ... (keep other parts) ...




        # 4. Product Categories
        self.stdout.write('4. Creating Categories...')
        categories_data = ['Electronics', 'Fashion', 'Home', 'Beauty', 'Sports', 'Toys', 'Books', 'Automotive']
        categories = []
        for name in categories_data:
            cat, _ = ProductCategory.objects.get_or_create(
                name=name,
                defaults={'icon_url': f'https://example.com/icons/{name.lower()}.png'}
            )
            categories.append(cat)

        # 5. Products & Related
        self.stdout.write('5. Creating Products & Inventory...')
        for i in range(25): # > 17 items
            name = f'Product {random_string(5)}'
            cat = random.choice(categories)
            price = Decimal(random.randint(10, 1000)) * 1000
            
            product = Product.objects.filter(name=name).first()
            if not product:
                product = Product.objects.create(
                    product_category=cat,
                    name=name,
                    size=Decimal(random.randint(1, 100)),
                    unit=random.choice(['cm', 'kg', 'g', 'pcs']),
                    description=f'This is a detailed description for {name}. It is very high quality.',
                    type=random.choice(['Type A', 'Type B', 'Standard']),
                    buy_price=price * Decimal('0.8'),
                    sell_price=price,
                    is_support_instant_delivery=random.choice([True, False]),
                    is_support_cod=random.choice([True, False]),
                    picture_url=f'https://example.com/products/{random_string(5)}.jpg',
                    tags='new,trending,bestseller'
                )
            
            # ProductInStore
            pis, _ = ProductInStore.objects.get_or_create(
                product=product,
                store=store,
                defaults={'stock': random.randint(10, 500), 'sold_count': random.randint(0, 50)}
            )

            # UserProductFavorite
            if i < 10:
                UserProductFavorite.objects.get_or_create(
                    product=product,
                    user=random.choice(users)
                )

            # ProductInStorePoint
            ProductInStorePoint.objects.get_or_create(
                product_in_store=pis,
                defaults={
                    'point_earned': random.randint(10, 100),
                    'datetime_started': past,
                    'datetime_ended': future
                }
            )

            # ProductInStoreDiscount
            discount, _ = ProductInStoreDiscount.objects.get_or_create(
                discount_label=f'Promo {random_string(3)}',
                defaults={'discount_precentage': Decimal(random.randint(5, 50))}
            )

            # Link Discount to Product
            if i % 3 == 0:
                ProductInStoreInProductInStoreDiscount.objects.get_or_create(
                    product_in_store=pis,
                    product_in_store_discount=discount,
                    defaults={'datetime_started': past, 'datetime_ended': future}
                )

        # 6. Flashsales
        self.stdout.write('6. Creating Flashsales...')
        flashsale, _ = Flashsale.objects.get_or_create(
            name='Super Flash Sale',
            defaults={
                'datetime_started': past,
                'datetime_ended': future
            }
        )
        
        # Link Products to Flashsale
        for pis in ProductInStore.objects.all()[:5]:
            ProductInStoreInFlashsale.objects.get_or_create(
                product_in_store=pis,
                flashsale=flashsale,
                defaults={
                    'discount_precentage': Decimal(70),
                    'stock': 10,
                    'sold_count': 0,
                    'quantity_limit': 1
                }
            )

        # 7. Carts
        self.stdout.write('7. Creating Carts...')
        # User Cart
        user_for_cart = users[0]
        user_cart, _ = UserCart.objects.get_or_create(user=user_for_cart)
        product_for_cart = Product.objects.first()
        ProductInUserCart.objects.get_or_create(
            product=product_for_cart,
            user_cart=user_cart,
            defaults={'quantity': 2, 'is_checked': True}
        )

        # Store Cart
        store_cart, _ = StoreCart.objects.get_or_create(
            name='Display Cart 1',
            store=store
        )
        ProductInStoreCart.objects.get_or_create(
            product=product_for_cart,
            store_cart=store_cart,
            defaults={'quantity': 5, 'is_checked': True}
        )

        # 8. Delivery & Orders
        self.stdout.write('8. Creating Delivery & Orders...')
        delivery_types = []
        for name, cost in [('JNE', 10000), ('GoSend', 20000), ('SiCepat', 12000)]:
            dt, _ = DeliveryType.objects.get_or_create(
                name=name,
                defaults={'cost': cost, 'discount': 0}
            )
            delivery_types.append(dt)

        payment_methods = []
        for name in ['BCA', 'OVO', 'COD']:
             pm, _ = PaymentMethod.objects.get_or_create(name=name, defaults={'fee': 1000})
             payment_methods.append(pm)

        for i in range(15): # > 7 orders
            user = random.choice(users)
            status_choice = random.choice(['pending', 'processed', 'shipped', 'finished', 'cancelled'])
            
            order = Order.objects.create(
                store=store,
                customer=user,
                address=user.addresses.first(),
                message_for_driver='Handle with care' if i % 2 == 0 else '',
                delivery_type=random.choice(delivery_types),
                status=status_choice,
                is_online_order=True,
                datetime_processed=now if status_choice != 'pending' else None,
                datetime_shipped=now if status_choice in ['shipped', 'finished'] else None,
                datetime_finished=now if status_choice == 'finished' else None,
                datetime_cancelled=now if status_choice == 'cancelled' else None
            )

            if status_choice in ['processed', 'shipped', 'finished']:
                order.cashier = admin_user
                order.save()
            
            if status_choice in ['shipped', 'finished']:
                order.driver = admin_user # Simulating driver
                order.save()

            # ProductInOrder
            prod = Product.objects.order_by('?').first()
            pio = ProductInOrder.objects.create(
                product=prod,
                order=order,
                quantity=random.randint(1, 5)
                # Optional fields like product_in_store_point could be linked here if complex logic used
            )

            # OrderPayment
            OrderPayment.objects.create(
                order=order,
                payment_method=random.choice(payment_methods),
                account_number=f'ACC-{random_digits(8)}',
                status='success' if status_choice != 'cancelled' else 'failed'
            )

            # Review (only if finished)
            if status_choice == 'finished':
                OrderReview.objects.create(
                    order=order,
                    rate=random.randint(1, 5),
                    comment='Great service!'
                )
                ProductInOrderReview.objects.create(
                    product_in_order=pio,
                    rate=random.randint(1, 5),
                    comment='Nice product.'
                )

        # 9. Wallet & Topup
        self.stdout.write('9. Creating Wallet History...')
        rule, _ = TopupWalletBalanceRule.objects.get_or_create(
            min_nominal_topup=10000,
            max_nominal_topup=1000000,
            point_earned=10,
            datetime_started=past,
            datetime_finished=future
        )

        for user in users[:5]:
            topup = UserTopupWalletBalance.objects.create(
                user=user,
                wallet=user.wallet,
                nominal_topup=50000,
                status='success',
                point_earned=10
            )
            UserTopupWalletBalancePayment.objects.create(
                topup_wallet_balance=topup,
                payment_method=random.choice(payment_methods),
                account_number='VA-12345',
                status='success'
            )
            
            # Transfer
            receiver = users[-1]
            if user != receiver:
                UserTransferWalletBalance.objects.create(
                    sender=user,
                    receiver=receiver,
                    nominal_transfer=10000,
                    admin_cost=500
                )
            
            # Payment Method saved
            UserPaymentMethod.objects.get_or_create(
                user=user,
                payment_method=random.choice(payment_methods),
                defaults={'account_number': '1234567890'}
            )

        # 10. Membership & Points
        self.stdout.write('10. Creating Membership & Points...')
        memberships = [
            (1, 'bronze', 0), (2, 'silver', 1000), (3, 'gold', 5000), (4, 'platinum', 10000)
        ]
        membership_objs = []
        for level, name, min_point in memberships:
            m, _ = Membership.objects.get_or_create(
                level=level,
                defaults={
                    'name': name,
                    'min_point_earned': min_point,
                    'description': f'{name} level benefits'
                }
            )
            membership_objs.append(m)

        # Reward
        reward, _ = PointMembershipReward.objects.get_or_create(
            point_earned=100,
            for_membership=membership_objs[0],
            defaults={'datetime_started': past, 'datetime_ended': future}
        )

        for user in users:
            # UserMembership
            um, _ = UserMembership.objects.get_or_create(
                user=user,
                defaults={
                    'referal_code': f'REF{user.id}',
                    'point': random.randint(0, 10000),
                    'membership': membership_objs[0]
                }
            )
            
            # History
            UserMembershipHistory.objects.get_or_create(
                user_membership=um,
                membership=membership_objs[0],
                defaults={'datetime_attached': past}
            )

            # Claim Reward
            if random.choice([True, False]):
                UserPointMembershipReward.objects.create(
                    user=user,
                    point_membership_reward=reward
                )

        # 11. Vouchers
        self.stdout.write('11. Creating Vouchers...')
        for i in range(10):
            vo, _ = VoucherOrder.objects.get_or_create(
                name=f'Mega Voucher {i}',
                defaults={
                    'source_type': 'code',
                    'description': 'Big discount',
                    'img_url': 'http://example.com/voucher.png',
                    'min_item_quantity': 1,
                    'min_item_cost': 50000,
                    'discount_precentage': 20,
                    'max_nominal_discount': 20000,
                    'datetime_started': past,
                    'datetime_expiry': future
                }
            )
            # Fix for OneToOne Field - access via related name or query
            if not VoucherOrderCode.objects.filter(voucher_order=vo).exists():
                VoucherOrderCode.objects.create(
                    voucher_order=vo,
                    code=f'SALE{i}{random_digits(3)}',
                    datetime_started=past, 
                    datetime_ended=future
                )
            
            # Assign to user
            UserVoucherOrder.objects.create(
                user=random.choice(users),
                voucher_order=vo,
                is_used=random.choice([True, False])
            )
            
            # Voucher Membership Reward
            VoucherOrderMembershipReward.objects.get_or_create(
                voucher_order=vo,
                for_membership=membership_objs[1], # Silver
                defaults={'datetime_started': past, 'datetime_ended': future}
            )
            
            # Voucher Point Redeem
            VoucherOrderPointReedem.objects.get_or_create(
                voucher_order=vo,
                point_required=500,
                min_membership_level=1
            )

        # 12. Netflix Points (Point App)
        self.stdout.write('12. Creating Netflix Point Redeems...')
        netflix, _ = NetflixDiscountPointReedem.objects.get_or_create(
            name='Netflix Subscription',
            defaults={
                'description': '1 Month Subscription',
                'point_required': 1000,
                'min_membership_level': 1,
                'netflix_discount_id': 'NETFLIX-001',
                'min_movie_cost': 0,
                'discount_precentage': 100,
                'max_nominal_discount': 50000
            }
        )
        
        UserNetflixDiscountPointReedem.objects.create(
            user=users[0],
            netflix_discount_reedem=netflix,
            datetime_reedem=now
        )

        self.stdout.write(self.style.SUCCESS('All models populated successfully with abundant data!'))
