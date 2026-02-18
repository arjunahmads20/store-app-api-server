from rest_framework import serializers
from .models import User, UserInbox, InvitationRule, UserInvitation, UserLog, OTPVerification

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'gender', 'date_of_birth', 'avatar_url', 'status', 'id_store_work_on']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

from django.core.validators import RegexValidator
from membership.models import UserMembership

class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    referral_code = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone_number', 
            'gender', 'date_of_birth', 'password', 'confirm_password', 'referral_code'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'phone_number': {'required': True},
            'gender': {'required': True},
            'date_of_birth': {'required': True},
        }

    def validate_phone_number(self, value):
        if not value.isdigit() or len(value) < 9 or len(value) > 15:
            raise serializers.ValidationError("Phone number must be numeric and between 9-15 digits.")
            
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number already registered.")
        return value
    
    def validate_referral_code(self, value):
        if value and not UserMembership.objects.filter(referral_code=value).exists():
             raise serializers.ValidationError("Invalid referral code.")
        return value

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({"password": "Password and Confirm Password do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        referral_code = validated_data.pop('referral_code', None)
        
        # Auto-generate username from phone number since it's unique and required by AbstractUser
        username = validated_data['phone_number']
        
        user = User.objects.create_user(username=username, **validated_data)
        
        # Store referral code temporarily for View to handle logic (e.g., rewarding points)
        user._referral_code = referral_code 
        return user

class UserInboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInbox
        fields = '__all__'

class InvitationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitationRule
        fields = '__all__'

class UserInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInvitation
        fields = '__all__'

class UserLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLog
        fields = '__all__'

class OTPVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPVerification
        fields = '__all__'
