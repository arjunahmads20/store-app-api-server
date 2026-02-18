from django.db import models

class DeliveryType(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    datetime_added = models.DateTimeField(auto_now_add=True)
    datetime_last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('shipped', 'Shipped'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled'),
    )

    store = models.ForeignKey('store.Store', on_delete=models.SET_NULL, null=True, related_name='orders')
    customer = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='orders')
    cashier = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_orders')
    driver = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='delivered_orders')
    address = models.ForeignKey('address.UserAddress', on_delete=models.SET_NULL, null=True)
    message_for_driver = models.TextField(null=True, blank=True)
    delivery_type = models.ForeignKey(DeliveryType, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_online_order = models.BooleanField(default=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_processed = models.DateTimeField(null=True, blank=True)
    datetime_shipped = models.DateTimeField(null=True, blank=True)
    datetime_cancelled = models.DateTimeField(null=True, blank=True)
    datetime_finished = models.DateTimeField(null=True, blank=True)

    def get_products(self):
        return self.products.all()

class ProductInOrder(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products')
    quantity = models.IntegerField(default=1)
    
    # Updated references to new store-specific models
    product_in_store_in_flashsale = models.ForeignKey('product.ProductInStoreInFlashsale', on_delete=models.SET_NULL, null=True, blank=True)
    product_in_store_in_product_in_store_discount = models.ForeignKey('product.ProductInStoreInProductInStoreDiscount', on_delete=models.SET_NULL, null=True, blank=True)
    product_in_store_point = models.ForeignKey('product.ProductInStorePoint', on_delete=models.SET_NULL, null=True, blank=True)

class OrderReview(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField()
    comment = models.TextField(null=True, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True)

class ProductInOrderReview(models.Model):
    product_in_order = models.ForeignKey(ProductInOrder, on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField()
    comment = models.TextField(null=True, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
