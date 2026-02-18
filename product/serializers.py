from rest_framework import serializers
from .models import (
    ProductCategory, Product, UserProductFavorite, 
    ProductInStore, ProductInStorePoint,
    ProductInStoreDiscount, ProductInStoreInProductInStoreDiscount, 
    Flashsale, ProductInStoreInFlashsale,
    UserCart, ProductInUserCart,
    StoreCart, ProductInStoreCart
)

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductInStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInStore
        fields = '__all__'

class UserProductFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProductFavorite
        fields = '__all__'

class ProductInStorePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInStorePoint
        fields = '__all__'

class ProductInStoreDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInStoreDiscount
        fields = '__all__'

class ProductInStoreInProductInStoreDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInStoreInProductInStoreDiscount
        fields = '__all__'

class FlashsaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashsale
        fields = '__all__'

class ProductInStoreInFlashsaleSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product_in_store.product.id') 
    class Meta:
        model = ProductInStoreInFlashsale
        fields = '__all__'

class UserCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCart
        fields = '__all__'
        read_only_fields = ['user']

class ProductInUserCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInUserCart
        fields = '__all__'
        read_only_fields = ['user_cart']

class StoreCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreCart
        fields = '__all__'

class ProductInStoreCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInStoreCart
        fields = '__all__'

# --- Aggregated Serializers ---
from django.db.models import Avg, Q
from django.utils import timezone
from order.models import ProductInOrderReview

class ComprehensiveProductSerializer(serializers.ModelSerializer):
    # Nested Info
    category = ProductCategorySerializer(source='product.product_category', read_only=True)
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(source='product.sell_price', max_digits=12, decimal_places=2)
    product_picture = serializers.URLField(source='product.picture_url')
    
    # Aggregated Info
    discount_info = serializers.SerializerMethodField()
    flashsale_info = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    
    # Requested Extensions
    product_tags = serializers.CharField(source='product.tags', read_only=True)
    point_earned = serializers.SerializerMethodField()

    # Size & Unit
    product_size = serializers.DecimalField(source='product.size', max_digits=8, decimal_places=2, read_only=True)
    product_unit = serializers.CharField(source='product.unit', read_only=True)
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = ProductInStore
        fields = [
            'id', 'store', 'product', 'category', 'product_name', 'product_price', 'product_picture',
            'product_tags', 'product_size', 'product_unit', 'display_name',
            'stock', 'sold_count', 
            'discount_info', 'flashsale_info', 'rating', 'is_favorite', 'point_earned'
        ]

    def get_display_name(self, obj):
        name = obj.product.name
        size = obj.product.size
        unit = obj.product.unit
        if size and unit:
            # Strip trailing zeros for cleaner display (e.g. 2.00 -> 2)
            size_str = f"{size:f}".rstrip('0').rstrip('.')
            return f"{name} {size_str} {unit}"
        return name

    def get_discount_info(self, obj):
        now = timezone.now()
        active_discounts = obj.productinstoreinproductinstorediscount_set.filter(
            datetime_started__lte=now,
            datetime_ended__gte=now
        )
        if active_discounts.exists():
            # Return the highest discount or list all? Requirement implies "the instance".
            # I'll return the first one for simplicity, or a list if multiple allowed.
            discount = active_discounts.first()
            return {
                'id': discount.product_in_store_discount.id,
                'label': discount.product_in_store_discount.discount_label,
                'percentage': discount.product_in_store_discount.discount_precentage,
                'datetime_ended': discount.datetime_ended
            }
        return None

    def get_flashsale_info(self, obj):
        now = timezone.now()
        active_flashsale = obj.productinstoreinflashsale_set.filter(
            flashsale__datetime_started__lte=now,
            flashsale__datetime_ended__gte=now
        ).first()
        if active_flashsale:
            return {
                'id': active_flashsale.flashsale.id,
                'name': active_flashsale.flashsale.name,
                'discount_percentage': active_flashsale.discount_precentage,
                'stock_left': active_flashsale.stock
            }
        return None
    
    def get_point_earned(self, obj):
        now = timezone.now()
        active_point = obj.productinstorepoint_set.filter(
            datetime_started__lte=now
        ).filter(
            Q(datetime_ended__gte=now) | Q(datetime_ended__isnull=True)
        ).order_by('-point_earned').first()
        
        if active_point:
            return active_point.point_earned
        return 0

    def get_rating(self, obj):
        # ProductInStore -> Product -> ProductInOrder -> ProductInOrderReview
        reviews = ProductInOrderReview.objects.filter(product_in_order__product=obj.product)
        avg_rating = reviews.aggregate(Avg('rate'))['rate__avg']
        return {
            'average_rate': round(avg_rating, 1) if avg_rating else 0,
            'review_count': reviews.count()
        }

    def get_is_favorite(self, obj):
        user = self.context.get('request').user
        if user and user.is_authenticated:
            return UserProductFavorite.objects.filter(user=user, product=obj.product).exists()
        return False
