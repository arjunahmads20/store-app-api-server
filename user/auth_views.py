from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from django.db import models
from django.utils import timezone
from .serializers import UserSerializer, UserRegistrationSerializer
from .models import User, UserInvitation, InvitationRule
from membership.models import UserMembership, Membership
from wallet.models import UserWallet
import random
import string

@api_view(['POST'])
@permission_classes([AllowAny])
def signup_request_otp(request):
    """
    Step 1: Validate User Data & Send OTP.
    """
    # 1. Validate User Data (Dry Run)
    serializer = UserRegistrationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    phone_number = request.data.get('phone_number')
    
    # 2. OTP Logic
    from .models import OTPVerification
    from django.conf import settings
    import random
    
    otp_instance = OTPVerification.objects.filter(phone_number=phone_number).first()
    otp_code = str(random.randint(100000, 999999))
    
    if not otp_instance:
        OTPVerification.objects.create(
            phone_number=phone_number,
            otp=otp_code,
            nm=settings.OTP_MINUTE_LIMIT,
            nd=settings.OTP_DAY_LIMIT
        )
        return Response({'message': 'OTP sent successfully.', 'otp': otp_code}, status=status.HTTP_200_OK)
    
    # Check Blocking
    is_blocked, msg = otp_instance.check_blocking()
    if is_blocked:
        return Response({'error': msg}, status=status.HTTP_403_FORBIDDEN)
    
    # Send Logic (Decrease counters on request? Logic say: "If time ... exceeded ... decrease nm and nd")
    # Actually logic says: Requesting Sending OTP -> Else (exists) -> If time diff > threshold -> decrease counters -> check 0 -> block OR send.
    # We need to check if we SHOULD decrease counters. 
    # Logic: "If the time since dm till now has exceed the specified threshold" -> This implies legitimate retry after block? 
    # OR does it mean "Rate limit check"? 
    # Usually: Requesting OTP *consumes* a token (counter).
    
    # Let's interpret "If time since dm...": It basically means "If not blocked (or block expired)". 
    # My helper check_blocking handles the expiration check.
    
    # Now execute the "decrease nm and nd" logic as per prompt
    blocked_msg = otp_instance.decrease_counters()
    if blocked_msg:
        # It became blocked JUST NOW
        return Response({'error': blocked_msg}, status=status.HTTP_403_FORBIDDEN)
        
    # If not blocked, Send
    otp_instance.otp = otp_code
    otp_instance.save()
    return Response({'message': 'OTP sent successfully.', 'otp': otp_code}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup_verify(request):
    """
    Step 2: Verify OTP & Create User.
    """
    # 1. Validate User Data (Again, for security)
    serializer = UserRegistrationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    phone_number = request.data.get('phone_number')
    otp_input = request.data.get('otp')
    
    if not otp_input:
        return Response({'error': 'OTP is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
    # 2. Verify OTP
    from .models import OTPVerification
    otp_instance = OTPVerification.objects.filter(phone_number=phone_number).first()
    
    if not otp_instance:
        return Response({'error': 'Please request OTP first.'}, status=status.HTTP_400_BAD_REQUEST)
        
    is_blocked, msg = otp_instance.check_blocking()
    if is_blocked:
        return Response({'error': msg}, status=status.HTTP_403_FORBIDDEN)
        
    if otp_instance.otp == otp_input:
        # Success!
        user = serializer.save() # Create User
        otp_instance.delete()    # Cleanup
        
        # 1. Automatic Wallet Creation
        # Generate a random unique account number
        account_number = ''.join(random.choices(string.digits, k=12))
        # Ensure uniqueness (simple check, retry if needed could be added but 10^12 is huge)
        while UserWallet.objects.filter(account_number=account_number).exists():
             account_number = ''.join(random.choices(string.digits, k=12))
             
        UserWallet.objects.create(user=user, account_number=account_number, balance=0)
        
        # 2. Automatic UserMembership Creation
        # Get Default Membership (Level 1 / Bronze)
        default_membership = Membership.objects.filter(level=1).first()
        
        # Generate Referral Code (e.g., REF<ID><RAND>)
        # Since ID is AutoField, we have it.
        ref_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        new_referral_code = f"REF{user.id}{ref_suffix}"
        
        # Ensure uniqueness
        while UserMembership.objects.filter(referal_code=new_referral_code).exists():
             ref_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
             new_referral_code = f"REF{user.id}{ref_suffix}"

        UserMembership.objects.create(
            user=user,
            membership=default_membership,
            referal_code=new_referral_code,
            point=0
        )

        # Handle Referral (Logic moved here from old signup)
        referral_code = getattr(user, '_referral_code', None)
        if referral_code:
            try:
                referrer_membership = UserMembership.objects.get(referal_code=referral_code)
                referrer = referrer_membership.user
                now = timezone.now()
                active_rule = InvitationRule.objects.filter(
                    datetime_started__lte=now
                ).filter(
                    models.Q(datetime_finished__isnull=True) | models.Q(datetime_finished__gte=now)
                ).first()
                if active_rule:
                    UserInvitation.objects.create(user=referrer, invitee=user, invitation_rule=active_rule)
            except UserMembership.DoesNotExist:
                pass 
                
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
        
    else:
        # Fail
        blocked_msg = otp_instance.decrease_counters()
        if blocked_msg:
             return Response({'error': blocked_msg}, status=status.HTTP_403_FORBIDDEN)
        return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Handles user login.
    - Authenticates via phone number and password.
    - Rewards inviter/invitee on first login if applicable.
    - Updates last_login timestamp.
    - Returns an auth token.
    """
    phone_number = request.data.get('phone_number')
    password = request.data.get('password')

    if not phone_number or not password:
         return Response({'error': 'Phone number and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Find user by phone number
    try:
        user = User.objects.get(phone_number=phone_number)
    except User.DoesNotExist:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

    # Verify password
    if user.check_password(password):
        # Check First Time Login
        if user.datetime_last_login is None:
            # Check for Invitation Reward
            invitation = UserInvitation.objects.filter(invitee=user, invitation_rule__isnull=False).first()
            if invitation:
                rule = invitation.invitation_rule
                inviter = invitation.user
                
                if rule.point_earned_by_inviter > 0:
                    try:
                        inviter_membership = UserMembership.objects.get(user=inviter)
                        inviter_membership.point += rule.point_earned_by_inviter
                        inviter_membership.save()
                    except UserMembership.DoesNotExist:
                        pass
                
                # If rule also rewards invitee
                if rule.point_earned_by_invitee > 0:
                     try:
                        invitee_membership = UserMembership.objects.get(user=user)
                        invitee_membership.point += rule.point_earned_by_invitee
                        invitee_membership.save()
                     except UserMembership.DoesNotExist:
                        pass
        
        # Update Last Login
        user.datetime_last_login = timezone.now()
        user.save()

        token, _ = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        return Response({'token': token.key, 'user': serializer.data})
    
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Handles user logout.
    - Deletes the current auth token.
    """
    try:
        request.user.auth_token.delete()
    except (AttributeError, Token.DoesNotExist):
        pass
    return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
