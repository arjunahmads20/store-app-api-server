from django.urls import path, include
from rest_framework_nested import routers
from .views import (
    ProductCategoryViewSet, ProductViewSet, UserProductFavoriteViewSet,
    ProductInStoreViewSet, ProductInStorePointViewSet, 
    ProductInStoreDiscountViewSet, ProductInStoreInProductInStoreDiscountViewSet,
    FlashsaleViewSet, ProductInStoreInFlashsaleViewSet, 
    UserCartViewSet, ProductInUserCartViewSet,
    StoreCartViewSet, ProductInStoreCartViewSet
)

# Main
router = routers.SimpleRouter()
router.register(r'product-categories', ProductCategoryViewSet, basename='productcategory')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'user-product-favorites', UserProductFavoriteViewSet, basename='userproductfavorite')
router.register(r'product-in-stores', ProductInStoreViewSet, basename='productinstore')
router.register(r'product-in-store-points', ProductInStorePointViewSet, basename='productinstorepoint')
router.register(r'product-in-store-discounts', ProductInStoreDiscountViewSet, basename='productinstorediscount')
router.register(r'product-in-store-in-product-in-store-discounts', ProductInStoreInProductInStoreDiscountViewSet) # -> Nested Now
router.register(r'flashsales', FlashsaleViewSet, basename='flashsale')
router.register(r'product-in-store-in-flashsales', ProductInStoreInFlashsaleViewSet) # -> Nested Now
router.register(r'user-carts', UserCartViewSet, basename='usercart')
router.register(r'store-carts', StoreCartViewSet, basename='storecart')

# Nested: UserCart -> Items
user_carts_router = routers.NestedSimpleRouter(router, r'user-carts', lookup='user_cart')
user_carts_router.register(r'product-in-user-carts', ProductInUserCartViewSet, basename='usercart-productinusercart')

# Nested: StoreCart -> Items
store_carts_router = routers.NestedSimpleRouter(router, r'store-carts', lookup='store_cart')
store_carts_router.register(r'product-in-store-carts', ProductInStoreCartViewSet, basename='storecart-productinstorecart')

# Nested: Flashsale -> Items
flashsales_router = routers.NestedSimpleRouter(router, r'flashsales', lookup='flashsale')
flashsales_router.register(r'product-in-store-in-flashsales', ProductInStoreInFlashsaleViewSet, basename='flashsale-productinstoreinflashsale')

# Nested: Discount -> Items
discounts_router = routers.NestedSimpleRouter(router, r'product-in-store-discounts', lookup='product_in_store_discount')
discounts_router.register(r'product-in-store-in-product-in-store-discounts', ProductInStoreInProductInStoreDiscountViewSet, basename='discount-items')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(user_carts_router.urls)),
    path('', include(store_carts_router.urls)),
    path('', include(flashsales_router.urls)),
    path('', include(discounts_router.urls)),
]
