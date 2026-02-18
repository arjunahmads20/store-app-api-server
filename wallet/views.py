from rest_framework import viewsets
from django.db import models
from .models import UserWallet, TopupWalletBalanceRule, UserTopupWalletBalance, UserTransferWalletBalance
from .serializers import (
    UserWalletSerializer, TopupWalletBalanceRuleSerializer, 
    UserTopupWalletBalanceSerializer, UserTransferWalletBalanceSerializer
)

from rest_framework.permissions import IsAuthenticated
from store_api_server.permissions import IsOwner

class UserWalletViewSet(viewsets.ModelViewSet):
    serializer_class = UserWalletSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        if self.request.user.is_staff:
            return UserWallet.objects.all()
        return UserWallet.objects.filter(user=self.request.user)

class TopupWalletBalanceRuleViewSet(viewsets.ModelViewSet):
    queryset = TopupWalletBalanceRule.objects.all()
    serializer_class = TopupWalletBalanceRuleSerializer
    permission_classes = [IsAuthenticated] # Read only for users usually?

class UserTopupWalletBalanceViewSet(viewsets.ModelViewSet):
    serializer_class = UserTopupWalletBalanceSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        if self.request.user.is_staff:
            return UserTopupWalletBalance.objects.all()
        return UserTopupWalletBalance.objects.filter(user=self.request.user)

class UserTransferWalletBalanceViewSet(viewsets.ModelViewSet):
    serializer_class = UserTransferWalletBalanceSerializer
    permission_classes = [IsAuthenticated] # Sender/Receiver logic complex for IsOwner simple check

    def get_queryset(self):
        # Users see transfers they sent or received
        user = self.request.user
        if user.is_staff:
            return UserTransferWalletBalance.objects.all()
        return UserTransferWalletBalance.objects.filter(models.Q(sender=user) | models.Q(receiver=user))
