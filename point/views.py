from rest_framework import viewsets
from .models import NetflixDiscountPointReedem, UserNetflixDiscountPointReedem, VoucherOrderPointReedem
from .serializers import (
    NetflixDiscountPointReedemSerializer, UserNetflixDiscountPointReedemSerializer, VoucherOrderPointReedemSerializer
)

from rest_framework.permissions import IsAuthenticated
from store_api_server.permissions import IsOwner

class NetflixDiscountPointReedemViewSet(viewsets.ModelViewSet):
    queryset = NetflixDiscountPointReedem.objects.all()
    serializer_class = NetflixDiscountPointReedemSerializer
    permission_classes = [IsAuthenticated]

class UserNetflixDiscountPointReedemViewSet(viewsets.ModelViewSet):
    serializer_class = UserNetflixDiscountPointReedemSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        if self.request.user.is_staff:
             return UserNetflixDiscountPointReedem.objects.all()
        return UserNetflixDiscountPointReedem.objects.filter(user=self.request.user)

class VoucherOrderPointReedemViewSet(viewsets.ModelViewSet):
    queryset = VoucherOrderPointReedem.objects.all()
    serializer_class = VoucherOrderPointReedemSerializer
