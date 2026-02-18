from django.contrib import admin
from .models import (
    ProductCategory, Product, ProductInStore, UserProductFavorite,
    ProductInStorePoint, ProductInStoreDiscount,
    ProductInStoreInProductInStoreDiscount, Flashsale,
    ProductInStoreInFlashsale, UserCart, ProductInUserCart,
    StoreCart, ProductInStoreCart
)

admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(ProductInStore)
admin.site.register(UserProductFavorite)
admin.site.register(ProductInStorePoint)
admin.site.register(ProductInStoreDiscount)
admin.site.register(ProductInStoreInProductInStoreDiscount)
admin.site.register(Flashsale)
admin.site.register(ProductInStoreInFlashsale)
admin.site.register(UserCart)
admin.site.register(ProductInUserCart)
admin.site.register(StoreCart)
admin.site.register(ProductInStoreCart)
