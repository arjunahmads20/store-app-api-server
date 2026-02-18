from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    icon_url = models.URLField(max_length=500, null=True, blank=True)
    datetime_added = models.DateTimeField(auto_now_add=True)
    datetime_last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    product_category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    size = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    unit = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True)
    buy_price = models.DecimalField(max_digits=12, decimal_places=2)
    sell_price = models.DecimalField(max_digits=12, decimal_places=2)
    is_support_instant_delivery = models.BooleanField(default=False)
    is_support_cod = models.BooleanField(default=False)
    picture_url = models.URLField(max_length=500, null=True, blank=True)
    tags = models.TextField(null=True, blank=True)
    datetime_added = models.DateTimeField(auto_now_add=True)
    datetime_last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductInStore(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    sold_count = models.PositiveIntegerField(default=0)
    datetime_added = models.DateTimeField(auto_now_add=True)
    datetime_last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} at {self.store.name}"

class UserProductFavorite(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    datetime_added = models.DateTimeField(auto_now_add=True)

class ProductInStorePoint(models.Model):
    product_in_store = models.ForeignKey(ProductInStore, on_delete=models.CASCADE)
    point_earned = models.PositiveIntegerField(default=0)
    datetime_added = models.DateTimeField(auto_now_add=True)
    datetime_last_updated = models.DateTimeField(auto_now=True)
    datetime_started = models.DateTimeField(null=True, blank=True)
    datetime_ended = models.DateTimeField(null=True, blank=True)

class ProductInStoreDiscount(models.Model):
    discount_label = models.CharField(max_length=100)
    discount_precentage = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    datetime_added = models.DateTimeField(auto_now_add=True)
    datetime_last_updated = models.DateTimeField(auto_now=True)

class ProductInStoreInProductInStoreDiscount(models.Model):
    product_in_store = models.ForeignKey(ProductInStore, on_delete=models.CASCADE)
    product_in_store_discount = models.ForeignKey(ProductInStoreDiscount, on_delete=models.CASCADE)
    datetime_added = models.DateTimeField(auto_now_add=True)
    datetime_started = models.DateTimeField(null=True, blank=True)
    datetime_ended = models.DateTimeField(null=True, blank=True)

class Flashsale(models.Model):
    name = models.CharField(max_length=255)
    banner_url = models.URLField(max_length=500, null=True, blank=True)
    datetime_added = models.DateTimeField(auto_now_add=True)
    datetime_last_updated = models.DateTimeField(auto_now=True)
    datetime_started = models.DateTimeField(null=True, blank=True)
    datetime_ended = models.DateTimeField(null=True, blank=True)

    def get_status(self):
        pass

class ProductInStoreInFlashsale(models.Model):
    product_in_store = models.ForeignKey(ProductInStore, on_delete=models.CASCADE)
    flashsale = models.ForeignKey(Flashsale, on_delete=models.CASCADE)
    discount_precentage = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default=0)
    sold_count = models.PositiveIntegerField(default=0)
    quantity_limit = models.PositiveIntegerField(default=0)
    datetime_added = models.DateTimeField(auto_now_add=True)
    datetime_last_updated = models.DateTimeField(auto_now=True)

class UserCart(models.Model):
    user = models.OneToOneField('user.User', on_delete=models.CASCADE)

class ProductInUserCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_cart = models.ForeignKey(UserCart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_checked = models.BooleanField(default=True)
    datetime_added = models.DateTimeField(auto_now_add=True)
    datetime_last_updated = models.DateTimeField(auto_now=True)

class StoreCart(models.Model):
    name = models.CharField(max_length=255)
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.store.name}"

class ProductInStoreCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    store_cart = models.ForeignKey(StoreCart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_checked = models.BooleanField(default=True)
    datetime_added = models.DateTimeField(auto_now_add=True)
    datetime_last_updated = models.DateTimeField(auto_now=True)

@receiver(post_save, sender=Product)
def create_product_in_stores(sender, instance, created, **kwargs):
    if created:
        Store = apps.get_model('store', 'Store')
        ProductInStore = apps.get_model('product', 'ProductInStore')
        
        stores = Store.objects.all()
        pis_list = []
        for store in stores:
            pis_list.append(ProductInStore(product=instance, store=store, stock=0))
        
        if pis_list:
            ProductInStore.objects.bulk_create(pis_list)
