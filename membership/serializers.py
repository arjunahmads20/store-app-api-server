from rest_framework import serializers
from .models import (
    Membership, UserMembership, UserMembershipHistory, 
    PointMembershipReward, UserPointMembershipReward, VoucherOrderMembershipReward
)

class MembershipSerializer(serializers.ModelSerializer):
    next_membership_name = serializers.SerializerMethodField()

    class Meta:
        model = Membership
        fields = '__all__'

    def get_next_membership_name(self, obj):
        try:
            next_level_membership = Membership.objects.get(level=obj.level + 1)
            return next_level_membership.name
        except Membership.DoesNotExist:
            return None

class UserMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMembership
        fields = '__all__'

class UserMembershipHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMembershipHistory
        fields = '__all__'

class PointMembershipRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointMembershipReward
        fields = '__all__'

class UserPointMembershipRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPointMembershipReward
        fields = '__all__'

class VoucherOrderMembershipRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoucherOrderMembershipReward
        fields = '__all__'


