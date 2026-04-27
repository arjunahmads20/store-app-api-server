# API Request & Response Schema Documentation

This document provides exhaustive JSON schemas for every resource, **linked to their specific API Endpoints and Actions**.

---

## 1. User App (`/api/v1/user/`)

### 1.1. Registration
#### 1.1.1. Request OTP (Signup)
**Endpoint**: `POST /signup/request-otp/`
**Action**: `signup_request_otp`
**Request Schema (`UserRegistrationSerializer`)**:
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone_number": "08123456789",
  "password": "secretpassword",
  "confirm_password": "secretpassword",
  "gender": "male",
  "date_of_birth": "1990-01-01",
  "referral_code": "INVITE123" // Optional
}
```
**Response Schema**:
```json
{
  "message": "OTP sent successfully.",
  "otp": "123456"
}
```

#### 1.1.2. Verify & Create User (Signup)
**Endpoint**: `POST /signup/verify/`
**Action**: `signup_verify`
**Request Schema**:
*Same as Request OTP, plus:*
```json
{
  "otp": "123456"
}
```
**Response Schema**:
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user": { ... }
}
```

### 1.2. Login
**Endpoint**: `POST /login/`
**Action**: `create` (Auth)
**Request Schema**:
```json
{
  "phone_number": "08123456789",
  "password": "secretpassword"
}
```
**Response Schema**:
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user": {
      "id": 1,
      "username": "08123456789",
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@example.com",
      "role": "customer",
      "status": "active",
      ...
  }
}
```

### 1.3. Logout
**Endpoint**: `POST /logout/`
**Action**: `create` (Auth)
**Response Schema**:
```json
{
  "message": "Successfully logged out."
}
```

### 1.4. User Resource
**Endpoint**: `GET /users/{id}/` (Retrieve) | `GET /users/` (List)
**Serializer**: `UserSerializer`
**Response Schema**:
```json
{
  "id": 1,
  "username": "08123456789",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone_number": "08123456789",
  "role": "customer",
  "gender": "male",
  "date_of_birth": "1990-01-01",
  "avatar_url": "http://example.com/avatar.jpg",
  "status": "active",
  "daily_product_quota": 10,
  "id_store_work_on": null,
  "datetime_last_login": "2023-01-01T10:00:00Z",
  "datetime_joined": "2023-01-01T09:00:00Z"
}
```

### 1.4. User Inbox
**Endpoint**: `GET /users/{id}/user-inboxes/`
**Action**: `list`
**Serializer**: `UserInboxSerializer`
**Response Schema**:
```json
{
  "id": 10,
  "user": 1,
  "subject": "Welcome",
  "body": "Welcome message...",
  "image_url": "http://...",
  "is_readed": false,
  "datetime_created": "2023-01-01T10:00:00Z",
  "datetime_readed": null
}
```

### 1.5. Invitation Rule
**Endpoint**: `GET /invitation-rules/`
**Action**: `list`
**Serializer**: `InvitationRuleSerializer`
**Response Schema**:
```json
{
  "id": 1,
  "point_earned_by_inviter": 500,
  "point_earned_by_invitee": 100,
  "datetime_started": "2023-01-01T00:00:00Z",
  "datetime_finished": null
}
```

### 1.6. User Invitation
**Endpoint**: `GET /users/{id}/user-invitations/`
**Action**: `list`
**Serializer**: `UserInvitationSerializer`
**Response Schema**:
```json
{
  "id": 5,
  "user": 1, 
  "invitee": 2, 
  "invitation_rule": 1,
  "datetime_accepted": "2023-01-02T10:00:00Z"
}
```

### 1.7. User Log
**Endpoint**: `GET /users/{id}/user-logs/`
**Action**: `list`
**Serializer**: `UserLogSerializer`
**Response Schema**:
```json
{
  "id": 100,
  "user": 1,
  "action": "LOGIN",
  "details": "User logged in via App",
  "datetime_created": "2023-01-01T10:00:00Z"
}
```

### 1.8. OTP Verification (Forgot Password / General)
#### 1.8.1. Request OTP
**Endpoint**: `POST /otp-verifications/send_otp/`
**Action**: `send_otp`
**Request Schema**:
```json
{
  "phone_number": "08123456789"
}
```
**Response Schema**:
```json
{
  "message": "OTP sent successfully.",
  "otp": "123456" // Dev/Test Mode only
}
```

#### 1.8.2. Verify OTP
**Endpoint**: `POST /otp-verifications/verify_otp/`
**Action**: `verify_otp`
**Request Schema**:
```json
{
  "phone_number": "08123456789",
  "otp": "123456"
}
```
**Response Schema**:
```json
{
  "message": "OTP verified successfully."
}
```

---

## 2. Store App (`/api/v1/store/`)

### 2.1. Store
**Endpoint**: `GET /stores/`
**Action**: `list`
**Serializer**: `StoreSerializer`
**Response Schema**:
```json
{
  "id": 1,
  "name": "Central Store",
  "street": 5,
  "village": 4,
  "street_name": "Jl. Ir. H. Juanda",
  "village_name": "Dago",
  "district_name": "Coblong",
  "lattitude": -6.123456,
  "longitude": 106.123456,
  "datetime_added": "2023-01-01T10:00:00Z",
  "datetime_last_updated": "2023-01-02T10:00:00Z"
}
```

---

## 3. Product App (`/api/v1/product/`)

### 3.1. Product Category
**Endpoint**: `GET /product-categories/`
**Action**: `list`
**Serializer**: `ProductCategorySerializer`
**Response Schema**:
```json
{
  "id": 1,
  "name": "Electronics",
  "icon_url": "http://..."
}
```

### 3.2. Product (Global)
**Endpoint**: `GET /products/`
**Action**: `list`
**Serializer**: `ProductSerializer`
**Response Schema**:
```json
{
  "id": 1,
  "name": "Iphone 18",
  "product_category": 1,
  "size": "2.00",
  "unit": "pcs",
  "buy_price": "100.00",
  "sell_price": "200.00",
  "tags": "electronics, mobile",
  "picture_url": "http://...",
  "description": "Description...",
  "is_support_cod": true,
  "is_support_instant_delivery": true
}
```

### 3.3. Store Inventory (Detailed)
**Endpoint**: `GET /product-in-stores/` (List) | `GET /product-in-stores/{id}/` (Retrieve)
**Action**: `list`, `retrieve`
**Serializer**: `ComprehensiveProductSerializer`
**Response Schema**:
```json
{
  "id": 10,
  "store": 1,
  "product": 1,
  "category": { "id": 1, "name": "Electronics", ... },
  "product_name": "Iphone 18",
  "product_price": "200.00",
  "product_picture": "http://...",
  "product_tags": "electronics, mobile",
  "product_size": "2.00",
  "product_unit": "kg",
  "display_name": "Iphone 18 2 kg",
  "stock": 50,
  "sold_count": 5,
  "discount_info": {
      "id": 1,
      "label": "Mega Sale",
      "percentage": "10.00",
      "datetime_ended": "2023-12-31T00:00:00Z"
  },
  "flashsale_info": {
      "id": 5,
      "name": "11.11",
      "discount_percentage": "50.00",
      "stock_left": 10
  },
  "rating": {
      "average_rate": 4.5,
      "review_count": 10
  },
  "is_favorite": true,
  "point_earned": 50
}
```

### 3.4. Store Inventory (Base)
**Endpoint**: `POST /product-in-stores/`
**Action**: `create`
**Serializer**: `ProductInStoreSerializer`
**Request Schema**:
```json
{
  "product": 1,
  "store": 1,
  "stock": 50,
  "sold_count": 0
}
```

### 3.5. User Favorite
**Endpoint**: `GET /user-product-favorites/`
**Action**: `list`
**Serializer**: `UserProductFavoriteSerializer`
**Response Schema**:
```json
{
  "id": 5,
  "product": 1,
  "user": 1,
  "datetime_added": "2023-01-01T10:00:00Z"
}
```

### 3.6. Flashsale Event
**Endpoint**: `GET /flashsales/`
**Action**: `list`
**Serializer**: `FlashsaleSerializer`
**Response Schema**:
```json
{
  "id": 1,
  "name": "11.11 Sale",
  "datetime_started": "2023-11-11T00:00:00Z",
  "datetime_ended": "2023-11-12T00:00:00Z"
}
```

### 3.7. Flashsale Items
**Endpoint**: `GET /flashsales/{id}/product-in-store-in-flashsales/`
**Action**: `list`
**Serializer**: `ProductInStoreInFlashsaleSerializer`
**Response Schema**:
```json
{
  "id": 20,
  "product_in_store": 10,
  "product_id": 2,
  "flashsale": 1,
  "discount_precentage": "50.00",
  "stock": 10,
  "sold_count": 2,
  "quantity_limit": 1
}
```

### 3.8. Store Discount Definitions
**Endpoint**: `GET /product-in-store-discounts/`
**Action**: `list`
**Serializer**: `ProductInStoreDiscountSerializer`
**Response Schema**:
```json
{
  "id": 1,
  "discount_label": "Clearance",
  "discount_precentage": "20.00"
}
```

### 3.9. Active Discount Items
**Endpoint**: `GET /product-in-store-discounts/{id}/product-in-store-in-product-in-store-discounts/`
**Action**: `list`
**Serializer**: `ProductInStoreInProductInStoreDiscountSerializer`
**Response Schema**:
```json
{
  "id": 5,
  "product_in_store": 10,
  "product_in_store_discount": 1,
  "datetime_started": "2023-01-01T00:00:00Z",
  "datetime_ended": "2023-02-01T00:00:00Z"
}
```

### 3.10. Product Points Rules
**Endpoint**: `GET /product-in-store-points/`
**Action**: `list`
**Serializer**: `ProductInStorePointSerializer`
**Response Schema**:
```json
{
  "id": 3,
  "product_in_store": 10,
  "point_earned": 50,
  "datetime_started": "2023-01-01T00:00:00Z",
  "datetime_ended": "2023-12-31T00:00:00Z"
}
```

### 3.11. User Cart
**Endpoint**: `GET /user-carts/`
**Action**: `list`
**Serializer**: `UserCartSerializer`
**Response Schema**:
```json
{
  "id": 1,
  "user": 1
}
```

### 3.12. Cart Items
**Endpoint**: `GET /user-carts/{id}/product-in-user-carts/`
**Action**: `list`
**Serializer**: `ProductInUserCartSerializer`
**Response Schema**:
```json
{
  "id": 5,
  "user_cart": 1,
  "product": 1,
  "quantity": 2,
  "is_checked": true
}
```

---

## 4. Order App (`/api/v1/order/`)

### 4.1. Delivery Types
**Endpoint**: `GET /delivery-types/`
**Action**: `list`
**Serializer**: `DeliveryTypeSerializer`
**Response Schema**:
```json
{
  "id": 1,
  "name": "Instant",
  "cost": "15000.00",
  "discount": "0.00"
}
```

### 4.2. Order Checkout (Validation)
**Endpoint**: `POST /orders/checkout/`
**Action**: `checkout`
**Request Schema**:
```json
{
  "store_id": 1,
  "user_voucher_order_id": 5 // Optional
}
```

### 4.3. Place Order
**Endpoint**: `POST /orders/`
**Action**: `create`
**Serializer**: `OrderSerializer` (Request)
**Request Schema**:
```json
{
  "store_id": 1,
  "address_id": 5,
  "delivery_type_id": 1,
  "payment_method_id": 2,
  "user_voucher_order_id": 5,
  "message_for_shopper": "Pack safely",
  "is_online_order": true
}
```

### 4.4. Order Details
**Endpoint**: `GET /orders/{id}/`
**Action**: `retrieve`
**Serializer**: `OrderSerializer` (Response - Computed)
**Response Schema**:
```json
{
  "id": 101,
  "store": 1,
  "customer": 1,
  "cashier": null,
  "driver": null,
  "address": 5,
  "delivery_type": { "id": 1, "name": "Instant", "cost": "15000.00" },
  "products": [
      {
          "id": 500,
          "order": 101,
          "product": { "id": 1, "name": "Iphone", ... },
          "quantity": 2,
          "product_in_store_point": 1,
          "product_in_store_in_flashsale": 1,
          "product_in_store_in_product_in_store_discount": 1,
          "flashsale_discount_percentage": "10.00",
          "product_discount_percentage": "5.00",
          "point_earned": 50
      }
  ],
  "payment_info": { 
      "id": 1,
      "order": 101,
      "payment_method": {
          "id": 2,
          "name": "Bank Transfer BCA",
          "fee": "5000.00",
          "discount": "0.00",
          "original_fee": "5000.00",
          "discounted_fee": 5000.00
      },
      "account_number": "VA-12345", 
      "transaction_token": "abcd123",
      "transaction_redirect_url": "https://app.examplepaymentgateway.com/snap/v2/pay?snap_token=abcd123",
      "status": "pending",
      "user_voucher_order": {
        "id": 5,
        "voucher_order": {
            "id": 1,
            "name": "Discount Voucher",
            "source_type": "code",
            "discount_precentage": "10.00",
            "max_nominal_discount": "50000.00"
        },
        "is_used": true,
        "datetime_added": "2023-01-01T10:00:00Z"
      },
      "datetime_created": "2023-01-01T12:00:00Z",
      "datetime_finished": null
  },
  "total_product_cost": 180000.00,
  "total_cost": 195000.00,
  "point_earned_total": 50,
  "status": "pending",
  "is_online_order": true,
  "message_for_driver": "Call upon arrival",
  "datetime_created": "2023-01-01T12:00:00Z",
  "datetime_processed": null,
  "datetime_shipped": null,
  "datetime_cancelled": null,
  "datetime_finished": null
}
```

### 4.5. Product In Order
**Endpoint**: `GET /orders/{id}/product-in-orders/`
**Action**: `list`
**Serializer**: `ProductInOrderSerializer`
**Response Schema**:
```json
{
  "id": 500,
  "order": 101,
  "product": { "id": 1, "name": "Iphone", ... },
  "quantity": 2,
  "product_in_store_point": 1,
  "product_in_store_in_flashsale": 1,
  "product_in_store_in_product_in_store_discount": 1,
  "flashsale_discount_percentage": "10.00",
  "product_discount_percentage": "5.00",
  "point_earned": 50
}
```

### 4.6. Order Reviews
**Endpoint**: `GET /orders/{id}/order-reviews/`
**Action**: `list`
**Serializer**: `OrderReviewSerializer`
**Response Schema**:
```json
{
  "id": 10,
  "order": 101,
  "rate": 5,
  "comment": "Excellent service!"
}
```

### 4.7. Product Reviews
**Endpoint**: `GET /product-in-order-reviews/`
**Action**: `list`
**Serializer**: `ProductInOrderReviewSerializer`
**Response Schema**:
```json
{
  "id": 20,
  "product_in_order": 500,
  "rate": 4,
  "comment": "Good product."
}
```

---

### 4.8. Cancel Order
**Endpoint**: `POST /orders/{id}/cancel/`
**Action**: `cancel`
**Serializer**: `OrderSerializer` (Response)
**Response Schema**: (Same as Order Details)

### 4.9. Process Order
**Endpoint**: `POST /orders/{id}/processed/`
**Action**: `processed`
**Permission**: Staff only
**Serializer**: `OrderSerializer` (Response)
**Response Schema**: (Same as Order Details)

### 4.10. Ship Order
**Endpoint**: `POST /orders/{id}/shipped/`
**Action**: `shipped`
**Permission**: Staff only
**Serializer**: `OrderSerializer` (Response)
**Response Schema**: (Same as Order Details)

### 4.11. Finish Order
**Endpoint**: `POST /orders/{id}/finish/`
**Action**: `finish`
**Serializer**: `OrderSerializer` (Response)
**Response Schema**: (Same as Order Details)

---

## 5. Wallet App (`/api/v1/wallet/`)

### 5.1. User Wallet
**Endpoint**: `GET /user-wallets/`
**Action**: `list`
**Serializer**: `UserWalletSerializer`
**Response Schema**:
```json
{
  "id": 1,
  "user": 1,
  "account_number": "WALLET-001",
  "pin_number": 123456,
  "balance": "500000.00"
}
```

### 5.2. Topup Rules
**Endpoint**: `GET /topup-wallet-balance-rules/`
**Action**: `list`
**Serializer**: `TopupWalletBalanceRuleSerializer`
**Response Schema**:
```json
{
  "id": 1,
  "min_nominal_topup": "100000.00",
  "max_nominal_topup": "1000000.00",
  "point_earned": 10
}
```

### 5.3. Topup Request
**Endpoint**: `POST /user-topup-wallet-balances/`
**Action**: `create`
**Serializer**: `UserTopupWalletBalanceSerializer`
**Response Schema**:
```json
{
  "id": 50,
  "user": 1,
  "wallet": 1,
  "nominal_topup": "100000.00",
  "status": "pending",
  "point_earned": 10,
  "datetime_created": "2023-01-01T12:00:00Z"
}
```

### 5.4. Transfer
**Endpoint**: `POST /user-transfer-wallet-balances/`
**Action**: `create`
**Serializer**: `UserTransferWalletBalanceSerializer`
**Response Schema**:
```json
{
  "id": 60,
  "sender": 1,
  "receiver": 2,
  "nominal_transfer": "50000.00",
  "admin_cost": "1000.00"
}
```

---

## 6. Membership App (`/api/v1/membership/`)

### 6.1. Membership Tiers
**Endpoint**: `GET /memberships/`
**Action**: `list`
**Serializer**: `MembershipSerializer`
**Response Schema**:
```json
{
  "id": 1,
  "level": 1,
  "name": "Bronze",
  "description": "Starter tier",
  "min_point_earned": 0,
  "next_membership_name": "Silver"
}
```

### 6.2. User Status
**Endpoint**: `GET /user-memberships/`
**Action**: `list`
**Serializer**: `UserMembershipSerializer`
**Response Schema**:
```json
{
  "id": 10,
  "user": 1,
  "membership": 1,
  "point": 1500,
  "level_up_point": 5000,
  "referal_code": "JOHN123",
  "datetime_attached": "2023-01-01T10:00:00Z",
  "datetime_ended": "2023-12-31T23:59:59Z"
}
```

### 6.3. Point Rewards
**Endpoint**: `GET /point-membership-rewards/`
**Action**: `list`
**Serializer**: `PointMembershipRewardSerializer`
**Response Schema**:
```json
{
  "id": 1,
  "point_earned": 1000,
  "for_membership": 2,
  "datetime_started": "2023-01-01T00:00:00Z",
  "datetime_ended": "2023-12-31T23:59:59Z"
}
```

### 6.4. Claimed Point Rewards
**Endpoint**: `GET /user-point-membership-rewards/`
**Action**: `list`
**Serializer**: `UserPointMembershipRewardSerializer`
**Response Schema**:
```json
{
  "id": 10,
  "user": 1,
  "point_membership_reward": 1,
  "datetime_claimed": "2023-02-01T10:00:00Z"
}
```

### 6.5. Voucher Rewards
**Endpoint**: `GET /voucher-order-membership-rewards/`
**Action**: `list`
**Serializer**: `VoucherOrderMembershipRewardSerializer`
**Response Schema**:
```json
{
  "id": 1,
  "voucher_order": 5,
  "for_membership": 3,
  "datetime_started": "2023-01-01T00:00:00Z",
  "datetime_ended": "2023-12-31T23:59:59Z"
}
```

### 6.6. All Membership Rewards (Combined)
**Endpoint**: `GET /membership-rewards/`
**Action**: `list`
**Serializer**: `PointMembershipRewardSerializer` or `VoucherOrderMembershipRewardSerializer`
**Response Schema**:
```json
[
    {
      "id": 1,
      "point_earned": 1000,
      "for_membership": 2,
      "datetime_started": "2023-01-01T00:00:00Z",
      "datetime_ended": "2023-12-31T23:59:59Z",
      "type": "point_reward"
    },
    {
      "id": 2,
      "voucher_order": 5,
      "for_membership": 3,
      "datetime_started": "2023-01-01T00:00:00Z",
      "datetime_ended": "2023-12-31T23:59:59Z",
      "type": "voucher_reward"
    }
]
```

---

## 7. Point App (`/api/v1/point/`)

### 7.1. Netflix Rules
**Endpoint**: `GET /netflix-discount-point-reedems/`
**Action**: `list`
**Serializer**: `NetflixDiscountPointReedemSerializer`
**Response Schema**:
```json
{
  "id": 1,
  "name": "Netflix 1 Month",
  "point_required": 5000,
  "min_membership": 2,
  "discount_precentage": "100.00"
}
```

### 7.2. User Redemptions
**Endpoint**: `GET /user-netflix-discount-point-reedems/`
**Action**: `list`
**Serializer**: `UserNetflixDiscountPointReedemSerializer`
**Response Schema**:
```json
{
  "id": 5,
  "user": 1,
  "netflix_discount_reedem": 1,
  "datetime_added": "2023-01-01T12:00:00Z"
}
```

### 7.3. Voucher Redemptions
**Endpoint**: `GET /voucher-order-point-reedems/`
**Action**: `list`
**Serializer**: `VoucherOrderPointReedemSerializer`
**Response Schema**:
```json
{
  "id": 2,
  "voucher_order": 6,
  "point_required": 2000,
  "min_membership": 1
}
```

---

## 8. Voucher App (`/api/v1/voucher/`)

### 8.1. Voucher Definitions
**Endpoint**: `GET /voucher-orders/`
**Action**: `list`
**Serializer**: `VoucherOrderSerializer`
**Response Schema**:
```json
{
  "id": 5,
  "name": "Welcome Discount",
  "source_type": "code",
  "min_item_quantity": 1,
  "discount_precentage": "10.00",
  "datetime_expiry": "2023-12-31T23:59:59Z"
}
```

### 8.2. My Vouchers
**Endpoint**: `GET /user-voucher-orders/`
**Action**: `list`
**Serializer**: `UserVoucherOrderSerializer`
**Response Schema**:
```json
{
  "id": 10,
  "user": 1,
  "voucher_order": 5,
  "is_used": false
}
```

### 8.3. Claim Voucher
**Endpoint**: `POST /user-voucher-orders/`
**Action**: `create`
**Request Schema**:
```json
{
  "voucher_order_id": 1,
  "code": "FRESH123" // Optional
}
```

---

## 9. Payment App (`/api/v1/payment/`)

### 9.1. Payment Methods
**Endpoint**: `GET /payment-methods/`
**Action**: `list`
**Serializer**: `PaymentMethodSerializer`
**Response Schema**:
```json
{
  "id": 1,
  "name": "Bank Transfer BCA",
  "fee": "5000.00",
  "discount": "0.00",
  "original_fee": "5000.00",
  "discounted_fee": 5000.00
}
```

### 9.2. User Methods
**Endpoint**: `GET /user-payment-methods/`
**Action**: `list`
**Serializer**: `UserPaymentMethodSerializer`
**Response Schema**:
```json
{
  "id": 2,
  "user": 1,
  "payment_method": 1,
  "account_number": "1234567890"
}
```

### 9.3. User Topup Wallet Balance Payments
**Endpoint**: `GET /user-topup-wallet-balance-payments/`
**Action**: `list`
**Serializer**: `UserTopupWalletBalancePaymentSerializer`
**Response Schema**:
```json
{
  "id": 50,
  "topup_wallet_balance": 100,
  "payment_method": {
      "id": 1,
      "name": "Bank Transfer BCA",
      "fee": "5000.00",
      "discount": "0.00",
      "original_fee": "5000.00",
      "discounted_fee": 5000.00
  },
  "account_number": "880123456789",
  "status": "pending",
  "datetime_created": "2023-01-01T12:00:00Z",
  "datetime_finished": null
}
```

### 9.4. Order Payments
**Endpoint**: `GET /order-payments/`
**Action**: `list`
**Serializer**: `OrderPaymentSerializer`
**Response Schema**:
```json
{
  "id": 1,
  "order": 101,
  "payment_method": {
      "id": 2,
      "name": "Bank Transfer BCA",
      "fee": "5000.00",
      "discount": "0.00",
      "original_fee": "5000.00",
      "discounted_fee": 5000.00
  },
  "account_number": "VA-12345", 
  "status": "pending",
  "user_voucher_order": {
      "id": 5,
      "voucher_order": {
          "id": 1,
          "name": "Discount Voucher",
          "source_type": "code",
          "discount_precentage": "10.00",
          "max_nominal_discount": "50000.00"
      },
      "is_used": true,
      "datetime_added": "2023-01-01T10:00:00Z"
  },
  "datetime_created": "2023-01-01T12:00:00Z",
  "datetime_finished": null
}
```

---

## 10. Address App (`/api/v1/address/`)

### 10.1. Regional Data
**Endpoint**: 
 `GET /countries/{id}/provinces/` or `GET /provinces/?country={id}`,
 `GET /countries/{cid}/provinces/{id}/regency-municipalities/`  or `GET /regency-municipalities/?country={id}&province={id}`,
 `GET /countries/{cid}/provinces/{pid}/regency-municipalities/{id}/districts/` or `GET /districts/?country={id}&province={id}&regency_municipality={id}`,
 `GET /countries/{cid}/provinces/{pid}/regency-municipalities/{rid}/districts/{id}/villages/` or `GET /villages/?country={id}&province={id}&regency_municipality={id}&district={id}`
**Action**: `list`
**Response Example (Village)**:
```json
{
  "id": 1000,
  "district": 500,
  "name": "Karet",
  "post_code": "12920"
}
```

### 10.2. User Address
**Endpoint**: `GET /user-addresses/`
**Action**: `list`
**Serializer**: `UserAddressSerializer`
**Response Schema**:
```json
{
  "id": 1,
  "user": 1,
  "village": 1000,
  "street": 50,
  "receiver_name": "John Doe",
  "receiver_phone_number": "08123456789",
  "lattitude": -6.12,
  "longitude": 106.12,
  "is_main_address": true,
  "is_office": false,
  "other_details": "Near the park",
  "village_detail": { "id": 1000, "name": "Karet", ... },
  "district_detail": { "id": 500, "name": "Setiabudi", ... },
  "regency_detail": { "id": 50, "name": "Jakarta Selatan", ... },
  "province_detail": { "id": 5, "name": "DKI Jakarta", ... },
  "country_detail": { "id": 1, "name": "Indonesia" },
  "street_detail": { "id": 50, "name": "Jalan Sudirman" }
}
```
