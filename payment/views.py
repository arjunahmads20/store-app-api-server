from rest_framework import viewsets
from .models import PaymentMethod, UserPaymentMethod, UserTopupWalletBalancePayment, OrderPayment
from .serializers import (
    PaymentMethodSerializer, UserPaymentMethodSerializer,
    UserTopupWalletBalancePaymentSerializer, OrderPaymentSerializer
)

from rest_framework.permissions import IsAuthenticated
from store_api_server.permissions import IsOwner

class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    ordering = ['id']
    permission_classes = [IsAuthenticated]

class UserPaymentMethodViewSet(viewsets.ModelViewSet):
    serializer_class = UserPaymentMethodSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        if self.request.user.is_staff:
            return UserPaymentMethod.objects.all()
        return UserPaymentMethod.objects.filter(user=self.request.user)

class UserTopupWalletBalancePaymentViewSet(viewsets.ModelViewSet):
    serializer_class = UserTopupWalletBalancePaymentSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        # Relates to Topup -> User
        if self.request.user.is_staff:
            return UserTopupWalletBalancePayment.objects.all()
        return UserTopupWalletBalancePayment.objects.filter(topup_wallet_balance__user=self.request.user)

class OrderPaymentViewSet(viewsets.ModelViewSet):
    serializer_class = OrderPaymentSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Relates to Order -> Customer
        if self.request.user.is_staff:
            return OrderPayment.objects.all()
        return OrderPayment.objects.filter(order__customer=self.request.user)
