from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps

class Store(models.Model):
    name = models.CharField(max_length=255)
    street = models.ForeignKey('address.Street', on_delete=models.SET_NULL, null=True, blank=True)
    village = models.ForeignKey('address.Village', on_delete=models.SET_NULL, null=True, blank=True)
    lattitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    datetime_added = models.DateTimeField(auto_now_add=True)
    datetime_last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

@receiver(post_save, sender=Store)
def create_product_in_stores(sender, instance, created, **kwargs):
    if created:
        Product = apps.get_model('product', 'Product')
        ProductInStore = apps.get_model('product', 'ProductInStore')
        
        products = Product.objects.all()
        pis_list = []
        for product in products:
            pis_list.append(ProductInStore(product=product, store=instance, stock=0))
        
        if pis_list:
            ProductInStore.objects.bulk_create(pis_list)
