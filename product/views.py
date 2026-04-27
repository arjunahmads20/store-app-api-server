from rest_framework import viewsets
from .models import (
    ProductCategory, Product, UserProductFavorite, 
    ProductInStore, ProductInStorePoint,
    ProductInStoreDiscount, ProductInStoreInProductInStoreDiscount, 
    Flashsale, ProductInStoreInFlashsale,
    UserCart, ProductInUserCart,
    StoreCart, ProductInStoreCart
)
from django.db.models import F
from .serializers import (
    ProductCategorySerializer, ProductSerializer, UserProductFavoriteSerializer,
    ProductInStoreSerializer, ProductInStorePointSerializer,
    ProductInStoreDiscountSerializer, ProductInStoreInProductInStoreDiscountSerializer,
    FlashsaleSerializer, ProductInStoreInFlashsaleSerializer,
    UserCartSerializer, ProductInUserCartSerializer,
    StoreCartSerializer, ProductInStoreCartSerializer
)
from rest_framework.permissions import IsAuthenticated
from store_api_server.permissions import IsOwner

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    ordering_fields = '__all__'
    ordering = ['id']

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ['product_category', 'type']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'buy_price', 'sell_price', 'datetime_added']
    ordering = ['id']

class ProductInStoreViewSet(viewsets.ModelViewSet):
    queryset = ProductInStore.objects.all()
    # Use Comprehensive serializer for 'list' and 'retrieve' to show full details
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            from .serializers import ComprehensiveProductSerializer
            return ComprehensiveProductSerializer
        return ProductInStoreSerializer
    
    from .filters import ProductFilter
    filterset_class = ProductFilter
    
    # Sorting fields mapping
    # Annotated fields in get_queryset allow cleaner sorting keys
    ordering_fields = ['name', 'sell_price', 'sold_count', 'category_name', 'datetime_added']
    ordering = ['id']
    
    # Standard search is handled by FilterSet 'search_keyword'
    search_fields = [] 

    def get_queryset(self):
        return ProductInStore.objects.select_related(
            'product', 'product__product_category', 'store'
        ).annotate(
            name=F('product__name'),
            sell_price=F('product__sell_price'),
            category_name=F('product__product_category__name')
        ).all()

class UserProductFavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = UserProductFavoriteSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    ordering = ['datetime_added']

    def get_queryset(self):
        if self.request.user.is_staff:
            return UserProductFavorite.objects.all()
        return UserProductFavorite.objects.filter(user=self.request.user)

class ProductInStorePointViewSet(viewsets.ModelViewSet):
    queryset = ProductInStorePoint.objects.all()
    serializer_class = ProductInStorePointSerializer
    ordering = ['id']

class ProductInStoreDiscountViewSet(viewsets.ModelViewSet):
    queryset = ProductInStoreDiscount.objects.all()
    serializer_class = ProductInStoreDiscountSerializer
    ordering = ['id']

class ProductInStoreInProductInStoreDiscountViewSet(viewsets.ModelViewSet):
    queryset = ProductInStoreInProductInStoreDiscount.objects.all()
    serializer_class = ProductInStoreInProductInStoreDiscountSerializer
    ordering = ['id']
    
    def get_queryset(self):
        parent_pk = self.kwargs.get('product_in_store_discount_pk')
        if parent_pk:
            return ProductInStoreInProductInStoreDiscount.objects.filter(product_in_store_discount_id=parent_pk)
        return super().get_queryset()

class FlashsaleViewSet(viewsets.ModelViewSet):
    queryset = Flashsale.objects.all()
    serializer_class = FlashsaleSerializer
    filterset_fields = {
        'datetime_started': ['gte', 'lte'],
        'datetime_ended': ['gte', 'lte']
    }
    ordering = ['-datetime_started']

class ProductInStoreInFlashsaleViewSet(viewsets.ModelViewSet):
    queryset = ProductInStoreInFlashsale.objects.all()
    serializer_class = ProductInStoreInFlashsaleSerializer

    from .filters import ProductInStoreInFlashsaleFilter
    filterset_class = ProductInStoreInFlashsaleFilter
    
    ordering = ['id']

    def get_queryset(self):
        parent_pk = self.kwargs.get('flashsale_pk')
        if parent_pk:
            return ProductInStoreInFlashsale.objects.filter(flashsale_id=parent_pk)
        return super().get_queryset()

class UserCartViewSet(viewsets.ModelViewSet):
    serializer_class = UserCartSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    ordering = ['id']

    def get_queryset(self):
        return UserCart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if UserCart.objects.filter(user=self.request.user).exists():
             raise ValidationError("You already have a cart.")
        serializer.save(user=self.request.user)

from rest_framework.exceptions import ValidationError

class ProductInUserCartViewSet(viewsets.ModelViewSet):
    serializer_class = ProductInUserCartSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filterset_fields = ['is_checked']
    ordering = ['-datetime_added']

    def get_queryset(self):
        parent_pk = self.kwargs.get('user_cart_pk')
        if parent_pk:
             return ProductInUserCart.objects.filter(user_cart_id=parent_pk, user_cart__user=self.request.user)
             
        return ProductInUserCart.objects.filter(user_cart__user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        product_id = self.request.data.get('product')
        quantity = int(self.request.data.get('quantity', 1))
        store_id = self.request.data.get('store_id') # Optional but good for specific stock check

        # 1. Get User Cart (or create)
        user_cart, _ = UserCart.objects.get_or_create(user=user)
        
        # 2. Check Daily Quota (Total quantity in cart + new quantity)
        # Note: Usually quota is checked at Checkout, but prompt asks for it here.
        current_cart_qty = sum(item.quantity for item in ProductInUserCart.objects.filter(user_cart=user_cart))
        if (current_cart_qty + quantity) > user.daily_product_quota:
             raise ValidationError(f"Exceeds daily quota of {user.daily_product_quota}")

        # 3. Check Product Stock
        # "requires the product_in_store instance"
        pis_query = ProductInStore.objects.filter(product_id=product_id, store_id=store_id)
        if not pis_query.exists():
            raise ValidationError("Impossible case: Product not found in store")

        # Check if any store has enough stock
        # If store_id was not provided, we check if *any* single store has enough, or total?
        # A cart item usually buys from a single source. Assuming we need at least one store with enough stock.
        available = False
        for pis in pis_query:
            if pis.stock >= quantity:
                available = True
                break
        
        if not available:
            # Calculate total just for error message
            total = sum(p.stock for p in pis_query)
            raise ValidationError(f"Insufficient stock. Max available in a store: {total}")

        # 4. Handle Duplicates (Update quantity if exists)
        existing_item = ProductInUserCart.objects.filter(user_cart=user_cart, product_id=product_id).first()
        if existing_item:
            existing_item.quantity += quantity
            existing_item.save()
            # Do not save serializer (it would create new), just return
            return
            
        serializer.save(user_cart=user_cart)

    def perform_update(self, serializer):
        # "Whether the product_in_cart instance is belong the user or not"
        # This is implicitly handled by get_queryset filtering by `user=self.request.user`.
        # If someone tries to update ID 5 but ID 5 belongs to another user, 404 Not Found occurs.
        # However, making it explicit if needed. 
        # Since get_queryset restricts access, we are safe. 
        # Verifying logic:
        instance = serializer.instance
        if instance.user_cart.user != self.request.user:
            raise ValidationError("You do not own this cart item.")
            
        # Optional: Re-check stock or quota? Prompt didn't ask, but good practice.
        # Leaving as strictly requested: "Things that will be checked ... belonging to user".
        serializer.save()

    def perform_destroy(self, instance):
        # "Whether the product_in_cart instance is belong the user or not"
        if instance.user_cart.user != self.request.user:
            raise ValidationError("You do not own this cart item.")
        instance.delete()

class StoreCartViewSet(viewsets.ModelViewSet):
    queryset = StoreCart.objects.all()
    serializer_class = StoreCartSerializer
    ordering = ['id']

class ProductInStoreCartViewSet(viewsets.ModelViewSet):
    queryset = ProductInStoreCart.objects.all()
    serializer_class = ProductInStoreCartSerializer
    ordering = ['id']

    def get_queryset(self):
        parent_pk = self.kwargs.get('store_cart_pk')
        if parent_pk:
            return ProductInStoreCart.objects.filter(store_cart_id=parent_pk)
        return super().get_queryset()
