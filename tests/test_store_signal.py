from django.test import TestCase
from store.models import Store
from product.models import Product, ProductCategory, ProductInStore
from decimal import Decimal

class StoreSignalTest(TestCase):
    def setUp(self):
        # Create a category
        self.category = ProductCategory.objects.create(name="Test Category")
        
        # Create some products
        self.p1 = Product.objects.create(
            name="Product 1", 
            product_category=self.category,
            buy_price=Decimal("100.00"), 
            sell_price=Decimal("120.00")
        )
        self.p2 = Product.objects.create(
            name="Product 2", 
            product_category=self.category,
            buy_price=Decimal("50.00"), 
            sell_price=Decimal("70.00")
        )

    def test_product_in_store_creation(self):
        # Verify no ProductInStore initially (for the store we are about to create)
        self.assertEqual(ProductInStore.objects.count(), 0)

        # Create a new Store
        new_store = Store.objects.create(name="New Test Store")

        # Check if ProductInStore instances were created for this store
        pis_count = ProductInStore.objects.filter(store=new_store).count()
        
        # Should match number of products
        self.assertEqual(pis_count, 2)
        
        # Verify details
        self.assertTrue(ProductInStore.objects.filter(store=new_store, product=self.p1).exists())
        self.assertTrue(ProductInStore.objects.filter(store=new_store, product=self.p2).exists())
        
        print("SUCCESS: ProductInStore instances automatically created for new Store.")
