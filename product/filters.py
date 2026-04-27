import django_filters
from django.db.models import Q, Case, When
from django.utils import timezone
from .models import ProductInStore, ProductInStoreInProductInStoreDiscount, ProductInStoreInFlashsale
from order.models import Order, ProductInOrder

class ProductFilter(django_filters.FilterSet):
    """
    Advanced filtering for ProductInStore.
    Includes filtering by Price, Category, Tags, Stock Status, Discount, Flashsale, and Recommendation.
    """
    # Basic Product Fields
    min_price = django_filters.NumberFilter(field_name="product__sell_price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="product__sell_price", lookup_expr='lte')
    category = django_filters.NumberFilter(field_name="product__product_category__id")
    category_name = django_filters.CharFilter(field_name="product__product_category__name", lookup_expr='icontains')
    tags = django_filters.CharFilter(field_name="product__tags", lookup_expr='icontains')
    
    # Flags
    is_in_stock = django_filters.BooleanFilter(method='filter_is_in_stock')
    is_support_cod = django_filters.BooleanFilter(field_name="product__is_support_cod")
    is_support_instant_delivery = django_filters.BooleanFilter(field_name="product__is_support_instant_delivery")
    
    # Discount / Flashsale
    is_in_discount = django_filters.BooleanFilter(method='filter_is_in_discount')
    discount_id = django_filters.NumberFilter(method='filter_discount_id')
    discount_label = django_filters.CharFilter(method='filter_discount_label')
    
    is_in_flashsale = django_filters.BooleanFilter(method='filter_is_in_flashsale')
    flashsale_id = django_filters.NumberFilter(field_name="productinstoreinflashsale__flashsale__id")

    # Recommended (Custom Logic)
    is_recommended = django_filters.BooleanFilter(method='filter_is_recommended')

    # Points
    is_contain_points = django_filters.BooleanFilter(method='filter_is_contain_points')

    # Search
    search_keyword = django_filters.CharFilter(method='filter_search_keyword')

    class Meta:
        model = ProductInStore
        fields = ['product', 'store']

    def filter_is_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        return queryset

    def filter_is_in_discount(self, queryset, name, value):
        now = timezone.now()
        if value:
            return queryset.filter(
                productinstoreinproductinstorediscount__datetime_started__lte=now,
                productinstoreinproductinstorediscount__datetime_ended__gte=now
            ).distinct()
        return queryset

    def filter_discount_id(self, queryset, name, value):
        now = timezone.now()
        return queryset.filter(
            productinstoreinproductinstorediscount__product_in_store_discount__id=value,
            productinstoreinproductinstorediscount__datetime_started__lte=now,
            productinstoreinproductinstorediscount__datetime_ended__gte=now
        ).distinct()

    def filter_discount_label(self, queryset, name, value):
        now = timezone.now()
        return queryset.filter(
            productinstoreinproductinstorediscount__product_in_store_discount__discount_label__icontains=value,
            productinstoreinproductinstorediscount__datetime_started__lte=now,
            productinstoreinproductinstorediscount__datetime_ended__gte=now
        ).distinct()

    def filter_is_in_flashsale(self, queryset, name, value):
        now = timezone.now()
        if value:
            return queryset.filter(
                productinstoreinflashsale__flashsale__datetime_started__lte=now,
                productinstoreinflashsale__flashsale__datetime_ended__gte=now
            ).distinct()
        return queryset

    def filter_is_recommended(self, queryset, name, value):
        """
        Filters products based on recommendation logic.
        - If anonymous: Return Best Sellers.
        - If authenticated:
            1. Fetch latest order.
            2. Match tags from bought products against available products.
            3. Sort by number of matched tags.
        """
        if not value:
            return queryset
            
        request = self.request
        if not request or not request.user.is_authenticated:
            # Fallback for anonymous: Best sellers
            return queryset.order_by('-sold_count')

        # 1. Get User's Latest Order Content
        last_order = Order.objects.filter(customer=request.user).order_by('-datetime_created').first()
        
        user_tags = set()
        if last_order:
            # Get products from this order
            pios = ProductInOrder.objects.filter(order=last_order).select_related('product')
            for pio in pios:
                p_tags = pio.product.tags
                if p_tags:
                    # Assuming comma separated tags or just a string. 
                    parts = [t.strip().lower() for t in p_tags.split(',')]
                    user_tags.update(parts)
        
        if not user_tags:
            # Fallback if no history or no tags
            return queryset.order_by('-sold_count')
            
        # 2. Score Products
        candidates = queryset.values('id', 'product__tags')
        
        scores = []
        for cand in candidates:
            c_tags_str = cand['product__tags']
            score = 0
            if c_tags_str:
                c_tags = set([t.strip().lower() for t in c_tags_str.split(',')])
                # Intersection count
                score = len(user_tags.intersection(c_tags))
            
            if score > 0:
                scores.append((cand['id'], score))
        
        # 3. Sort by Score Descending
        scores.sort(key=lambda x: x[1], reverse=True)
        
        if not scores:
             # No matches found, fallback
             return queryset.order_by('-sold_count')

        # Limit to top results
        top_scores = scores[:50]
        top_ids = [x[0] for x in top_scores]
        
        # 4. Preserve Order in QuerySet
        preserved_order = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(top_ids)])
        
        return queryset.filter(pk__in=top_ids).order_by(preserved_order)

    def filter_is_contain_points(self, queryset, name, value):
        now = timezone.now()
        if value:
            return queryset.filter(
                productinstorepoint__datetime_started__lte=now,
                productinstorepoint__point_earned__gt=0
            ).filter(
                Q(productinstorepoint__datetime_ended__gte=now) | 
                Q(productinstorepoint__datetime_ended__isnull=True)
            ).distinct()
        return queryset

    def filter_search_keyword(self, queryset, name, value):
        return queryset.filter(
            Q(product__name__icontains=value) | 
            Q(product__product_category__name__icontains=value) |
            Q(product__description__icontains=value) |
            Q(product__tags__icontains=value)
        ).distinct()

class ProductInStoreInFlashsaleFilter(django_filters.FilterSet):
    flashsale = django_filters.NumberFilter(field_name="flashsale__id")
    store = django_filters.NumberFilter(field_name="product_in_store__store__id")
    
    class Meta:
        model = ProductInStoreInFlashsale
        fields = []