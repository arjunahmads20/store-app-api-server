import os
import django
from django.utils import timezone
from datetime import timedelta
import sys

# Setup Django environment
sys.path.append('c:\\Users\\arjunahmad\\Project\\Store_2')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store_api_server.settings')
django.setup()

from store.models import Store
from product.models import Product, ProductInStore, Flashsale, ProductInStoreInFlashsale, ProductCategory
from product.serializers import ComprehensiveProductSerializer

def test_flashsale_info():
    print("Setting up test data...")
    
    # 1. Create dependencies
    category, _ = ProductCategory.objects.get_or_create(name="Test Category")
    store, _ = Store.objects.get_or_create(name="Test Store", defaults={'village_id': 1, 'street': None})
    
    # 2. Create Product
    product, _ = Product.objects.get_or_create(
        name="Test Product Flashsale",
        defaults={
            'sell_price': 10000,
            'buy_price': 8000,
            'product_category': category
        }
    )
    
    # 3. Create ProductInStore
    pis, _ = ProductInStore.objects.get_or_create(
        store=store,
        product=product,
        defaults={'stock': 100, 'price': 10000}
    )
    
    # 4. Create Active Flashsale
    now = timezone.now()
    flashsale, _ = Flashsale.objects.get_or_create(
        name="Test Flashsale",
        defaults={
            'datetime_started': now - timedelta(hours=1),
            'datetime_ended': now + timedelta(hours=1)
        }
    )
    
    # Ensure dates cover 'now' if it already existed
    flashsale.datetime_started = now - timedelta(hours=1)
    flashsale.datetime_ended = now + timedelta(hours=1)
    flashsale.save()
    
    # 5. Link Product to Flashsale
    pis_flashsale, _ = ProductInStoreInFlashsale.objects.get_or_create(
        product_in_store=pis,
        flashsale=flashsale,
        defaults={
            'discount_precentage': 50,
            'stock': 10
        }
    )
    
    print(f"ProductInStore ID: {pis.id}")
    print(f"Flashsale ID: {flashsale.id}")
    print(f"ProductInStoreInFlashsale ID: {pis_flashsale.id}")
    print(f"Current Time: {now}")
    
    # 6. Serialize
    from unittest.mock import Mock
    request = Mock()
    request.user = None
    serializer = ComprehensiveProductSerializer(pis, context={'request': request})
    data = serializer.data
    
    print("\nSerialized Data:")
    print(f"Product Name: {data.get('product_name')}")
    print(f"Flashsale Info: {data.get('flashsale_info')}")
    
    if data.get('flashsale_info') is None:
        print("\nFAIL: flashsale_info is None")
    else:
        print("\nSUCCESS: flashsale_info is present")

if __name__ == "__main__":
    test_flashsale_info()
