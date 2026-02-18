import django_filters
from .models import PointMembershipReward, UserPointMembershipReward, VoucherOrderMembershipReward
from voucher.models import UserVoucherOrder

class PointMembershipRewardFilter(django_filters.FilterSet):
    is_claimed = django_filters.BooleanFilter(method='filter_is_claimed')

    class Meta:
        model = PointMembershipReward
        fields = []

    def filter_is_claimed(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            claimed_ids = UserPointMembershipReward.objects.filter(user=user).values_list('point_membership_reward_id', flat=True)
            if value:
                return queryset.filter(id__in=claimed_ids)
            else:
                return queryset.exclude(id__in=claimed_ids)
        return queryset

class VoucherOrderMembershipRewardFilter(django_filters.FilterSet):
    is_claimed = django_filters.BooleanFilter(method='filter_is_claimed')

    class Meta:
        model = VoucherOrderMembershipReward
        fields = []

    def filter_is_claimed(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            # For voucher rewards, we check if the user has claimed the associated voucher order
            # The structure is: UserVoucherOrder -> VoucherOrder <- VoucherOrderMembershipReward
            
            # 1. Get VoucherOrders claimed by user
            claimed_voucher_order_ids = UserVoucherOrder.objects.filter(user=user).values_list('voucher_order_id', flat=True)
            
            # 2. Filter VoucherOrderMembershipReward based on whether their voucher_order is in that list
            if value:
                return queryset.filter(voucher_order__id__in=claimed_voucher_order_ids)
            else:
                return queryset.exclude(voucher_order__id__in=claimed_voucher_order_ids)
        return queryset
