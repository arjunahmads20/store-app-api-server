from rest_framework import viewsets
from .models import (
    Membership, UserMembership, UserMembershipHistory, 
    PointMembershipReward, UserPointMembershipReward, VoucherOrderMembershipReward
)
from .serializers import (
    MembershipSerializer, UserMembershipSerializer, UserMembershipHistorySerializer,
    PointMembershipRewardSerializer, UserPointMembershipRewardSerializer, VoucherOrderMembershipRewardSerializer
)

from rest_framework.permissions import IsAuthenticated
from store_api_server.permissions import IsOwner

# Additional imports required for MembershipRewardViewSet
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status
from django.utils import timezone
from .filters import PointMembershipRewardFilter, VoucherOrderMembershipRewardFilter
from .services import MembershipSystem

class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all().order_by('level')
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['level']

class MembershipRewardViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        now = timezone.now()
        user = request.user
        try:
             user_membership = UserMembership.objects.get(user=user)
        except UserMembership.DoesNotExist:
             return Response([], status=status.HTTP_200_OK)

        # 1. Point Rewards
        point_rewards = PointMembershipReward.objects.filter(
            Q(datetime_started__lte=now) | Q(datetime_started__isnull=True),
            Q(datetime_ended__gte=now) | Q(datetime_ended__isnull=True),
            for_membership=user_membership.membership
        )
        point_rewards = PointMembershipRewardFilter(request.GET, queryset=point_rewards, request=request).qs
        point_data = PointMembershipRewardSerializer(point_rewards, many=True).data
        for item in point_data:
            item['type'] = 'point_reward'

        # 2. Voucher Rewards
        voucher_rewards = VoucherOrderMembershipReward.objects.filter(
            Q(datetime_started__lte=now) | Q(datetime_started__isnull=True),
            Q(datetime_ended__gte=now) | Q(datetime_ended__isnull=True),
            for_membership=user_membership.membership
        )
        voucher_rewards = VoucherOrderMembershipRewardFilter(request.GET, queryset=voucher_rewards, request=request).qs
        voucher_data = VoucherOrderMembershipRewardSerializer(voucher_rewards, many=True).data
        for item in voucher_data:
            item['type'] = 'voucher_reward'

        combined_data = point_data + voucher_data
        return Response(combined_data)

class UserMembershipViewSet(viewsets.ModelViewSet):
    serializer_class = UserMembershipSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return UserMembership.objects.all()
        return UserMembership.objects.filter(user=self.request.user)

class UserMembershipHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = UserMembershipHistorySerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        if self.request.user.is_staff:
            return UserMembershipHistory.objects.all()
        return UserMembershipHistory.objects.filter(user_membership__user=self.request.user)

class PointMembershipRewardViewSet(viewsets.ModelViewSet):
    queryset = PointMembershipReward.objects.all()
    serializer_class = PointMembershipRewardSerializer

class UserPointMembershipRewardViewSet(viewsets.ModelViewSet):
    serializer_class = UserPointMembershipRewardSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def create(self, request, *args, **kwargs):
        from django.db import transaction
        from django.utils import timezone
        from rest_framework.exceptions import ValidationError
        from .models import UserMembership,PointMembershipReward, UserPointMembershipReward
        with transaction.atomic():
            user = request.user
            point_membership_reward_id = request.data.get('point_membership_reward_id')
            now = timezone.now()
            try:
                point_membership_reward = PointMembershipReward.objects.get(id=point_membership_reward_id)
            except PointMembershipReward.DoesNotExist:
                raise ValidationError("Invalid point membership reward.")
            user_membership = UserMembership.objects.get(user=user)
            # Check the membership
            if point_membership_reward.for_membership != user_membership.membership:
                raise ValidationError("Membership is not valid for this point membership reward.")
            # Check the date
            if point_membership_reward.datetime_started:
                if point_membership_reward.datetime_started > now:
                    raise ValidationError("The reward has not been started ")
            if point_membership_reward.datetime_ended:
                if point_membership_reward.datetime_ended < now:
                    raise ValidationError("The reward has expired ")
            
            # Check if the user already claimed
            if UserPointMembershipReward.objects.filter(user=user, point_membership_reward=point_membership_reward).exists():
                raise ValidationError("You have already claimed this reward.")
            
            # Create the user point membership reward
            user_point_membership_reward = UserPointMembershipReward.objects.create(
                user=user,
                point_membership_reward=point_membership_reward
            )
            # Update the user membership point
            user_membership.earn_point(point_membership_reward.point_earned)
            # Update Membership Level
            MembershipSystem.update(user_membership)

            serializer = self.get_serializer(user_point_membership_reward)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        if self.request.user.is_staff:
             return UserPointMembershipReward.objects.all()
        return UserPointMembershipReward.objects.filter(user=self.request.user)

class VoucherOrderMembershipRewardViewSet(viewsets.ModelViewSet):
    queryset = VoucherOrderMembershipReward.objects.all()
    serializer_class = VoucherOrderMembershipRewardSerializer
