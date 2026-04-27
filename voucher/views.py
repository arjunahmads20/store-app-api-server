from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from store_api_server.permissions import IsOwner
from .models import VoucherOrder, VoucherOrderCode, UserVoucherOrder
from .serializers import VoucherOrderSerializer, VoucherOrderCodeSerializer, UserVoucherOrderSerializer

from membership.models import UserMembership, VoucherOrderMembershipReward
from point.models import VoucherOrderPointReedem
from .filters import VoucherOrderFilter, UserVoucherOrderFilter

class VoucherOrderViewSet(viewsets.ModelViewSet):
    queryset = VoucherOrder.objects.all()
    serializer_class = VoucherOrderSerializer
    filterset_class = VoucherOrderFilter

class VoucherOrderCodeViewSet(viewsets.ModelViewSet):
    queryset = VoucherOrderCode.objects.all()
    serializer_class = VoucherOrderCodeSerializer

class UserVoucherOrderViewSet(viewsets.ModelViewSet):
    serializer_class = UserVoucherOrderSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    filter_backends = [DjangoFilterBackend]
    filterset_class = UserVoucherOrderFilter

    ordering = ['-voucher_order__datetime_expiry']

    def create(self, request, *args, **kwargs):
        from django.db import transaction
        
        with transaction.atomic():
            user = request.user
            voucher_order_id = request.data.get("voucher_order_id")
            now = timezone.now()
            if not voucher_order_id:
                code = request.data.get("code")
                try:
                    voucher_order_code = VoucherOrderCode.objects.get(code=code)
                except VoucherOrderCode.DoesNotExist:
                    raise ValidationError("Invalid voucher code.")
                voucher_order = voucher_order_code.voucher_order
                # Check the date of the voucher order
                if voucher_order.datetime_started:
                    if voucher_order.datetime_started > now:
                        raise ValidationError("The voucher order has not been started")
                if voucher_order.datetime_expiry:
                    if voucher_order.datetime_expiry < now:
                        raise ValidationError("The voucher order has expired")
                # Check the date of the voucher order code
                if voucher_order_code.datetime_started:
                    if voucher_order_code.datetime_started > now:
                        raise ValidationError("The code has not been started")
                if voucher_order_code.datetime_ended:
                    if voucher_order_code.datetime_ended < now:
                        raise ValidationError("The code has expired")
            else:
                try:
                    voucher_order = VoucherOrder.objects.get(id=voucher_order_id)
                except VoucherOrder.DoesNotExist:
                    raise ValidationError("Invalid voucher code.")

                # Check the date of the voucher order
                if voucher_order.datetime_started:
                    if voucher_order.datetime_started > now:
                        raise ValidationError("Voucher order has not been started.")
                if voucher_order.datetime_expiry:
                    if voucher_order.datetime_expiry < now:
                        raise ValidationError("Voucher order has expired.")
            
            

                if voucher_order.source_type == "membership_reward":
                    try:
                        voucher_order_membership_reward = VoucherOrderMembershipReward.objects.get(voucher_order__id=voucher_order_id)
                    except VoucherOrderMembershipReward.DoesNotExist:
                        raise ValidationError("Invalid voucher code.")
                    user_membership = UserMembership.objects.get(user=user)
                    # Check the membership
                    if voucher_order_membership_reward.for_membership != user_membership.membership:
                        raise ValidationError("Membership is not valid for this voucher.")
                    # Check the date
                    if voucher_order_membership_reward.datetime_started:
                        if voucher_order_membership_reward.datetime_started > now:
                            raise ValidationError("The reward has not been started ")
                    if voucher_order_membership_reward.datetime_ended:
                        if voucher_order_membership_reward.datetime_ended < now:
                            raise ValidationError("The reward has expired ")

                elif voucher_order.source_type == "point_reedem":
                    try:
                        voucher_order_point_reedem = VoucherOrderPointReedem.objects.get(voucher_order__id=voucher_order_id)
                    except VoucherOrderPointReedem.DoesNotExist:
                        raise ValidationError("Invalid voucher code.")
                    user_membership = UserMembership.objects.get(user=user)
                    # Check the membership
                    if voucher_order_point_reedem.min_membership.level > user_membership.level:
                        raise ValidationError("Membership is not valid for this voucher.")
                    # Check the membership point
                    if voucher_order_point_reedem.point_required > user_membership.point:
                        raise ValidationError("Not enough points for this voucher.")
                    # Check the date
                    if voucher_order_point_reedem.datetime_started:
                        if voucher_order_point_reedem.datetime_started > now:
                            raise ValidationError("The reedem has not been started.")

                    # Update the membership point
                    user_membership.point -= voucher_order_point_reedem.point_required
                    user_membership.save()

            # Check if user already claimed
            if UserVoucherOrder.objects.filter(user=user, voucher_order=voucher_order).exists():
                raise ValidationError("You have already claimed this voucher.")

            # Create the user voucher order
            user_voucher_order = UserVoucherOrder.objects.create(user=user, voucher_order=voucher_order)
            
            serializer = self.get_serializer(user_voucher_order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

            

        

   
    def get_queryset(self):
        if self.request.user.is_staff:
             return UserVoucherOrder.objects.all()
        return UserVoucherOrder.objects.filter(user=self.request.user)
