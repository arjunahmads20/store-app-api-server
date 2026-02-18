from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to access it.
    Assumes the model has a `user` or `customer` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Admin can access everything
        if request.user.is_staff:
            return True

        # 1. Direct User Instance Check
        # Using simple class name check or isinstance if we imported User model, but simple check avoids circular import issues
        if obj.__class__.__name__ == 'User':
            return obj == request.user

        # 2. Standard 'user' field (Covers most models: Inbox, Cart, Wallet, etc.)
        if hasattr(obj, 'user'):
            # Special case for Invitation/Transfer where 'user' might be sender but we might allow receiver too
            # We handle that below specifically if needed, but for simple 'user' field:
            if obj.user == request.user:
                return True

        # 3. 'customer' field (Order)
        if hasattr(obj, 'customer'):
            if obj.customer == request.user:
                return True

        # 4. 'invitee' field (UserInvitation)
        if hasattr(obj, 'invitee'):
            if obj.invitee == request.user:
                return True

        # 5. 'sender' / 'receiver' (UserTransferWalletBalance)
        if hasattr(obj, 'sender') and obj.sender == request.user:
            return True
        if hasattr(obj, 'receiver') and obj.receiver == request.user:
            return True

        # 6. Nested relationships
        # ProductInUserCart -> user_cart -> user
        if hasattr(obj, 'user_cart') and hasattr(obj.user_cart, 'user'):
            return obj.user_cart.user == request.user
            
        # ProductInOrder -> order -> customer
        if hasattr(obj, 'order') and hasattr(obj.order, 'customer'):
            return obj.order.customer == request.user

        # UserMembershipHistory -> user_membership -> user
        if hasattr(obj, 'user_membership') and hasattr(obj.user_membership, 'user'):
            return obj.user_membership.user == request.user

        # UserTopupWalletBalancePayment -> topup_wallet_balance -> user
        if hasattr(obj, 'topup_wallet_balance') and hasattr(obj.topup_wallet_balance, 'user'):
            return obj.topup_wallet_balance.user == request.user
            
        return False
