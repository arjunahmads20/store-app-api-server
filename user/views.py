from rest_framework import viewsets
from rest_framework.decorators import action
from .models import User, UserInbox, InvitationRule, UserInvitation, UserLog, OTPVerification
from .serializers import (
    UserSerializer, UserInboxSerializer, InvitationRuleSerializer, 
    UserInvitationSerializer, UserLogSerializer, OTPVerificationSerializer
)

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from store_api_server.permissions import IsOwner

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Allow creating (signup) handled separately or AllowAny for POST? 
    # Usually standard ModelViewSet create is protected if we want strict control, 
    # but we have a separate signup endpoint. 
    # Let's say: List/Retrieve/Update/Delete requires IsOwner or Admin.
    permission_classes = [IsAuthenticated, IsOwner]

    @action(detail=False, methods=['get', 'put', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        
        elif request.method in ['PUT', 'PATCH']:
            serializer = self.get_serializer(user, data=request.data, partial=request.method == 'PATCH')
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

class UserInboxViewSet(viewsets.ModelViewSet):
    serializer_class = UserInboxSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        user_pk = self.kwargs.get('user_pk')
        if user_pk:
             return UserInbox.objects.filter(user_id=user_pk)
        return UserInbox.objects.filter(user=self.request.user)

class InvitationRuleViewSet(viewsets.ModelViewSet):
    queryset = InvitationRule.objects.all()
    serializer_class = InvitationRuleSerializer
    permission_classes = [IsAuthenticated]

class UserInvitationViewSet(viewsets.ModelViewSet):
    serializer_class = UserInvitationSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        user_pk = self.kwargs.get('user_pk')
        if user_pk:
            # Ambiguous: sent or received? Assuming sent as it's under 'users/id/invitations'
            return UserInvitation.objects.filter(models.Q(user_id=user_pk) | models.Q(invitee_id=user_pk))
            
        # Users see invitations sent by them or received by them
        user = self.request.user
        return UserInvitation.objects.filter(models.Q(user=user) | models.Q(invitee=user))

class UserLogViewSet(viewsets.ModelViewSet):
    serializer_class = UserLogSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        user_pk = self.kwargs.get('user_pk')
        if user_pk:
             return UserLog.objects.filter(user_id=user_pk)

        if self.request.user.is_staff:
            return UserLog.objects.all()
        return UserLog.objects.filter(user=self.request.user)

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
import random

class OTPVerificationViewSet(viewsets.ModelViewSet):
    queryset = OTPVerification.objects.all()
    serializer_class = OTPVerificationSerializer
    
    @action(detail=False, methods=['post'])
    def send_otp(self, request):
        # Case: Forgot Password / General Verification
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'error': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)

        otp_instance = OTPVerification.objects.filter(phone_number=phone_number).first()
        otp_code = str(random.randint(100000, 999999))

        if not otp_instance:
            OTPVerification.objects.create(
                phone_number=phone_number,
                otp=otp_code,
                nm=settings.OTP_MINUTE_LIMIT,
                nd=settings.OTP_DAY_LIMIT
            )
            print(f"OTP Code: {otp_code}")
            return Response({'message': 'OTP sent successfully.', '(For debug purpose) otp': otp_code}, status=status.HTTP_200_OK)
        
        # Check Blocking
        is_blocked, msg = otp_instance.check_blocking()
        if is_blocked:
            return Response({'error': msg}, status=status.HTTP_403_FORBIDDEN)
            
        # Decrease Counters logic (Rate limiting request)
        blocked_msg = otp_instance.decrease_counters()
        if blocked_msg:
             return Response({'error': blocked_msg}, status=status.HTTP_403_FORBIDDEN)
             
        # Send
        otp_instance.otp = otp_code
        otp_instance.save()
        print(f"OTP Code: {otp_code}")
        return Response({'message': 'OTP sent successfully.', '(For debug purpose) otp': otp_code}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def verify_otp(self, request):
        phone_number = request.data.get('phone_number')
        otp_input = request.data.get('otp')
        
        if not phone_number or not otp_input:
             return Response({'error': 'Phone number and OTP are required.'}, status=status.HTTP_400_BAD_REQUEST)
             
        otp_instance = OTPVerification.objects.filter(phone_number=phone_number).first()
        if not otp_instance:
             return Response({'error': 'Please request OTP first.'}, status=status.HTTP_404_NOT_FOUND)
        
        is_blocked, msg = otp_instance.check_blocking()
        if is_blocked:
            return Response({'error': msg}, status=status.HTTP_403_FORBIDDEN)
            
        if otp_instance.otp == otp_input:
            otp_instance.delete()
            return Response({'message': 'OTP verified successfully.'}, status=status.HTTP_200_OK)
        else:
            blocked_msg = otp_instance.decrease_counters()
            if blocked_msg:
                 return Response({'error': blocked_msg}, status=status.HTTP_403_FORBIDDEN)
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
