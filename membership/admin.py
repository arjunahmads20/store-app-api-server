from django.contrib import admin
from .models import (
    Membership, UserMembership, UserMembershipHistory,
    PointMembershipReward, UserPointMembershipReward,
    VoucherOrderMembershipReward
)

admin.site.register(Membership)
admin.site.register(UserMembership)
admin.site.register(UserMembershipHistory)
admin.site.register(PointMembershipReward)
admin.site.register(UserPointMembershipReward)
admin.site.register(VoucherOrderMembershipReward)
