import django_filters
from .models import VoucherOrder, UserVoucherOrder
from django.db.models import Q

class VoucherOrderFilter(django_filters.FilterSet):
    is_claimed = django_filters.BooleanFilter(method='filter_is_claimed')

    class Meta:
        model = VoucherOrder
        fields = ['source_type']

    def filter_is_claimed(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            claimed_ids = UserVoucherOrder.objects.filter(user=user).values_list('voucher_order_id', flat=True)
            if value:
                return queryset.filter(id__in=claimed_ids)
            else:
                return queryset.exclude(id__in=claimed_ids)
        return queryset

from django.utils import timezone

class UserVoucherOrderFilter(django_filters.FilterSet):
    is_expired = django_filters.BooleanFilter(method='filter_is_expired')

    class Meta:
        model = UserVoucherOrder
        fields = ['is_used']

    def filter_is_expired(self, queryset, name, value):
        now = timezone.now()
        if value:
            return queryset.filter(voucher_order__datetime_expiry__lt=now)
        else:
            return queryset.filter(
                Q(voucher_order__datetime_expiry__gte=now) | 
                Q(voucher_order__datetime_expiry__isnull=True)
            )
