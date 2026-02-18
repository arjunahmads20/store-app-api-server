from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MembershipViewSet, UserMembershipViewSet, UserMembershipHistoryViewSet,
    PointMembershipRewardViewSet, UserPointMembershipRewardViewSet, VoucherOrderMembershipRewardViewSet,
    MembershipRewardViewSet
)

router = DefaultRouter()
router.register(r'memberships', MembershipViewSet, basename='membership')
router.register(r'user-memberships', UserMembershipViewSet, basename='usermembership')
router.register(r'user-membership-histories', UserMembershipHistoryViewSet, basename='usermembershiphistory')
router.register(r'point-membership-rewards', PointMembershipRewardViewSet, basename='pointmembershipreward')
router.register(r'user-point-membership-rewards', UserPointMembershipRewardViewSet, basename='userpointmembershipreward')
router.register(r'voucher-order-membership-rewards', VoucherOrderMembershipRewardViewSet, basename='voucherordermembershipreward')
router.register(r'membership-rewards', MembershipRewardViewSet, basename='membershipreward')

urlpatterns = [
    path('', include(router.urls)),
]
