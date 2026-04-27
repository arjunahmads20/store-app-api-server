# Exhaustive Entity Relationship Documentation

This document lists every single model and field defined in the Store API Server.

## 1. User App (`user`)

### `User`
*Custom User model extending AbstractUser.*
*   `id`: AutoField (PK)
*   `username`: CharField
*   `password`: CharField
*   `first_name`: CharField
*   `last_name`: CharField
*   `email`: EmailField
*   `phone_number`: CharField (Unique, Nullable)
*   `is_email_verified`: BooleanField (Default: False)
*   `datetime_email_verified`: DateTimeField (Nullable)
*   `gender`: CharField (Choices: Male, Female, Other, Nullable)
*   `date_of_birth`: DateField (Nullable)
*   `avatar_url`: URLField (Nullable)
*   `status`: CharField (Default: 'active')
*   `role`: CharField (Choices: Customer, Driver, Admin, Default: 'customer')
*   `daily_product_quota`: PositiveSmallIntegerField (Default: 10)
*   `id_store_work_on`: ForeignKey -> `store.Store` (Nullable, Related: 'staff')
*   `datetime_last_login`: DateTimeField (Nullable)
*   `datetime_joined`: DateTimeField (auto_now_add=True)

### `UserInbox`
*   `id`: AutoField (PK)
*   `user`: ForeignKey -> `User`
*   `subject`: CharField
*   `body`: TextField
*   `image_url`: URLField (Nullable)
*   `is_readed`: BooleanField (Default: False)
*   `datetime_created`: DateTimeField (auto_now_add=True)
*   `datetime_readed`: DateTimeField (Nullable)

### `InvitationRule`
*   `id`: AutoField (PK)
*   `point_earned_by_inviter`: PositiveIntegerField (Default: 0)
*   `point_earned_by_invitee`: PositiveIntegerField (Default: 0)
*   `datetime_added`: DateTimeField (auto_now_add=True)
*   `datetime_last_updated`: DateTimeField (auto_now=True)
*   `datetime_started`: DateTimeField (Nullable)
*   `datetime_finished`: DateTimeField (Nullable)

### `UserInvitation`
*   `id`: AutoField (PK)
*   `user`: ForeignKey -> `User` (Inviter)
*   `invitee`: ForeignKey -> `User` (Invitee)
*   `invitation_rule`: ForeignKey -> `InvitationRule` (Nullable)
*   `datetime_accepted`: DateTimeField (auto_now_add=True)

### `UserLog`
*   `id`: AutoField (PK)
*   `user`: ForeignKey -> `User`
*   `action`: CharField
*   `details`: TextField (Nullable)
*   `datetime_created`: DateTimeField (auto_now_add=True)

### `OTPVerification`
*   `id`: AutoField (PK)
*   `phone_number`: CharField
*   `otp`: CharField
*   `is_verified`: BooleanField (Default: False)
*   `is_otp_blocked`: BooleanField (Default: False)
*   `nm`: PositiveSmallIntegerField
*   `nd`: PositiveSmallIntegerField
*   `dm`: DateTimeField (Nullable)
*   `dd`: DateTimeField (Nullable)
*   `datetime_created`: DateTimeField (auto_now_add=True)
*   `datetime_verified`: DateTimeField (Nullable)

---

## 2. Store App (`store`)

### `Store`
*Physical store location.*
*   `id`: AutoField (PK)
*   `name`: CharField
*   `street`: ForeignKey -> `address.Street` (Nullable)
*   `village`: ForeignKey -> `address.Village` (Nullable)
*   `lattitude`: DecimalField(9,6) (Nullable)
*   `longitude`: DecimalField(9,6) (Nullable)
*   `datetime_added`: DateTimeField (auto_now_add=True)
*   `datetime_last_updated`: DateTimeField (auto_now=True)

---

## 3. Product App (`product`)

### `ProductCategory`
*   `id`: AutoField (PK)
*   `name`: CharField
*   `icon_url`: URLField (Nullable)
*   `datetime_added`: DateTimeField (auto_now_add=True)
*   `datetime_last_updated`: DateTimeField (auto_now=True)

### `Product`
*Global product definition.*
*   `id`: AutoField (PK)
*   `product_category`: ForeignKey -> `ProductCategory` (Nullable)
*   `name`: CharField
*   `size`: DecimalField(8,2) (Nullable)
*   `unit`: CharField (Nullable)
*   `description`: TextField (Nullable)
*   `type`: CharField (Nullable)
*   `buy_price`: DecimalField(12,2)
*   `sell_price`: DecimalField(12,2)
*   `is_support_instant_delivery`: BooleanField (Default: False)
*   `is_support_cod`: BooleanField (Default: False)
*   `picture_url`: URLField (Nullable)
*   `tags`: TextField (Nullable)
*   `datetime_added`: DateTimeField (auto_now_add=True)
*   `datetime_last_updated`: DateTimeField (auto_now=True)

### `ProductInStore`
*Inventory at a specific store.*
*   `id`: AutoField (PK)
*   `product`: ForeignKey -> `Product`
*   `store`: ForeignKey -> `store.Store`
*   `stock`: PositiveIntegerField (Default: 0)
*   `sold_count`: PositiveIntegerField (Default: 0)
*   `datetime_added`: DateTimeField (auto_now_add=True)
*   `datetime_last_updated`: DateTimeField (auto_now=True)

### `UserProductFavorite`
*   `id`: AutoField (PK)
*   `product`: ForeignKey -> `Product`
*   `user`: ForeignKey -> `user.User`
*   `datetime_added`: DateTimeField (auto_now_add=True)

### `ProductInStorePoint`
*   `id`: AutoField (PK)
*   `product_in_store`: ForeignKey -> `ProductInStore`
*   `point_earned`: PositiveIntegerField (Default: 0)
*   `datetime_added`: DateTimeField (auto_now_add=True)
*   `datetime_last_updated`: DateTimeField (auto_now=True)
*   `datetime_started`: DateTimeField (Nullable)
*   `datetime_ended`: DateTimeField (Nullable)

### `ProductInStoreDiscount`
*   `id`: AutoField (PK)
*   `discount_label`: CharField
*   `discount_precentage`: DecimalField(8,2) (Default: 0)
*   `datetime_added`: DateTimeField (auto_now_add=True)
*   `datetime_last_updated`: DateTimeField (auto_now=True)

### `ProductInStoreInProductInStoreDiscount`
*   `id`: AutoField (PK)
*   `product_in_store`: ForeignKey -> `ProductInStore`
*   `product_in_store_discount`: ForeignKey -> `ProductInStoreDiscount`
*   `datetime_added`: DateTimeField (auto_now_add=True)
*   `datetime_started`: DateTimeField (Nullable)
*   `datetime_ended`: DateTimeField (Nullable)

### `Flashsale`
*   `id`: AutoField (PK)
*   `name`: CharField
*   `datetime_added`: DateTimeField (auto_now_add=True)
*   `datetime_last_updated`: DateTimeField (auto_now=True)
*   `datetime_started`: DateTimeField (Nullable)
*   `datetime_ended`: DateTimeField (Nullable)

### `ProductInStoreInFlashsale`
*   `id`: AutoField (PK)
*   `product_in_store`: ForeignKey -> `ProductInStore`
*   `flashsale`: ForeignKey -> `Flashsale`
*   `discount_precentage`: DecimalField(8,2) (Default: 0)
*   `stock`: PositiveIntegerField (Default: 0)
*   `sold_count`: PositiveIntegerField (Default: 0)
*   `quantity_limit`: PositiveIntegerField (Default: 0)
*   `datetime_added`: DateTimeField (auto_now_add=True)
*   `datetime_last_updated`: DateTimeField (auto_now=True)

### `Cart`
*   `id`: AutoField (PK)
*   `user`: OneToOneField -> `user.User`

### `ProductInCart`
*   `id`: AutoField (PK)
*   `product`: ForeignKey -> `Product`
*   `cart`: ForeignKey -> `Cart`
*   `quantity`: PositiveIntegerField (Default: 1)
*   `is_checked`: BooleanField (Default: True)
*   `datetime_added`: DateTimeField (auto_now_add=True)
*   `datetime_last_updated`: DateTimeField (auto_now=True)

### `StoreCart`
*   `id`: AutoField (PK)
*   `name`: CharField
*   `store`: ForeignKey -> `store.Store`

### `ProductInStoreCart`
*   `id`: AutoField (PK)
*   `product`: ForeignKey -> `Product`
*   `store_cart`: ForeignKey -> `StoreCart`
*   `quantity`: PositiveIntegerField (Default: 1)
*   `is_checked`: BooleanField (Default: True)
*   `datetime_added`: DateTimeField (auto_now_add=True)
*   `datetime_last_updated`: DateTimeField (auto_now=True)

---

## 4. Order App (`order`)

### `DeliveryType`
*   `id`: AutoField (PK)
*   `name`: CharField
*   `cost`: DecimalField(12,2)
*   `discount`: DecimalField(12,2) (Default: 0)
*   `datetime_added`: DateTimeField (auto_now_add=True)
*   `datetime_last_updated`: DateTimeField (auto_now=True)

### `Order`
*   `id`: AutoField (PK)
*   `store`: ForeignKey -> `store.Store` (Nullable)
*   `customer`: ForeignKey -> `user.User`
*   `cashier`: ForeignKey -> `user.User` (Nullable)
*   `driver`: ForeignKey -> `user.User` (Nullable)
*   `address`: ForeignKey -> `address.UserAddress` (Nullable)
*   `delivery_type`: ForeignKey -> `DeliveryType` (Nullable)
*   `message_for_driver`: TextField (Nullable)
*   `status`: CharField (Choices: Pending, Processed, Shipped, Finished, Cancelled)
*   `is_online_order`: BooleanField (Default: True)
*   `datetime_created`: DateTimeField (auto_now_add=True)
*   `datetime_processed`: DateTimeField (Nullable)
*   `datetime_shipped`: DateTimeField (Nullable)
*   `datetime_finished`: DateTimeField (Nullable)
*   `datetime_cancelled`: DateTimeField (Nullable)

### `ProductInOrder`
*   `id`: AutoField (PK)
*   `product`: ForeignKey -> `product.Product`
*   `order`: ForeignKey -> `Order`
*   `quantity`: IntegerField
*   `product_in_store_point`: ForeignKey -> `product.ProductInStorePoint` (Nullable)
*   `product_in_store_in_flashsale`: ForeignKey -> `product.ProductInStoreInFlashsale` (Nullable)
*   `product_in_store_in_product_in_store_discount`: ForeignKey -> `product.ProductInStoreInProductInStoreDiscount` (Nullable)

### `OrderReview`
*   `id`: AutoField (PK)
*   `order`: ForeignKey -> `Order`
*   `rate`: PositiveSmallIntegerField
*   `comment`: TextField (Nullable)
*   `datetime_created`: DateTimeField (auto_now_add=True)

### `ProductInOrderReview`
*   `id`: AutoField (PK)
*   `product_in_order`: ForeignKey -> `ProductInOrder`
*   `rate`: PositiveSmallIntegerField
*   `comment`: TextField (Nullable)
*   `datetime_created`: DateTimeField (auto_now_add=True)

---

## 5. Wallet App (`wallet`)

### `UserWallet`
*   `id`: AutoField (PK)
*   `user`: OneToOneField -> `user.User`
*   `account_number`: CharField (Unique)
*   `balance`: DecimalField(12,2) (Default: 0)

### `TopupWalletBalanceRule`
*   `id`: AutoField (PK)
*   `min_nominal_topup`: DecimalField(12,2)
*   `max_nominal_topup`: DecimalField(12,2)
*   `point_earned`: IntegerField
*   `datetime_added`: DateTimeField (auto_now_add=True)
*   `datetime_last_updated`: DateTimeField (auto_now=True)
*   `datetime_started`: DateTimeField (Nullable)
*   `datetime_finished`: DateTimeField (Nullable)

### `UserTopupWalletBalance`
*   `id`: AutoField (PK)
*   `user`: ForeignKey -> `user.User`
*   `wallet`: ForeignKey -> `UserWallet`
*   `nominal_topup`: DecimalField(12,2)
*   `status`: CharField (Default: 'pending')
*   `point_earned`: IntegerField (Default: 0)
*   `datetime_created`: DateTimeField (auto_now_add=True)
*   `datetime_finished`: DateTimeField (Nullable)

### `UserTransferWalletBalance`
*   `id`: AutoField (PK)
*   `sender`: ForeignKey -> `user.User`
*   `receiver`: ForeignKey -> `user.User`
*   `nominal_transfer`: DecimalField(12,2)
*   `admin_cost`: DecimalField(12,2) (Default: 0)
*   `datetime_created`: DateTimeField (auto_now_add=True)
*   `datetime_finished`: DateTimeField (Nullable)

---

## 6. Membership App (`membership`)

### `Membership`
*   `id`: AutoField (PK)
*   `level`: PositiveSmallIntegerField (Unique)
*   `name`: CharField (Unique)
*   `description`: TextField (Nullable)
*   `min_point_earned`: PositiveIntegerField (Default: 0)

### `UserMembership`
*   `id`: AutoField (PK)
*   `user`: OneToOneField -> `user.User`
*   `membership`: ForeignKey -> `Membership` (Nullable)
*   `point`: PositiveIntegerField (Default: 0)
*   `referal_code`: CharField (Unique, Nullable)
*   `level_up_point`: PositiveIntegerField (Default: 0)
*   `datetime_attached`: DateTimeField (auto_now_add=True)
*   `datetime_ended`: DateTimeField (Nullable)

### `UserMembershipHistory`
*   `id`: AutoField (PK)
*   `user_membership`: ForeignKey -> `UserMembership`
*   `membership`: ForeignKey -> `Membership`
*   `datetime_attached`: DateTimeField
*   `datetime_ended`: DateTimeField (Nullable)

### `PointMembershipReward`
*   `id`: AutoField (PK)
*   `point_earned`: PositiveIntegerField
*   `for_membership`: ForeignKey -> `Membership`
*   `datetime_started`: DateTimeField (Nullable)
*   `datetime_ended`: DateTimeField (Nullable)

### `UserPointMembershipReward`
*   `id`: AutoField (PK)
*   `user`: ForeignKey -> `user.User`
*   `point_membership_reward`: ForeignKey -> `PointMembershipReward`
*   `datetime_claimed`: DateTimeField (auto_now_add=True)

### `VoucherOrderMembershipReward`
*   `id`: AutoField (PK)
*   `voucher_order`: OneToOneField -> `voucher.VoucherOrder`
*   `for_membership`: ForeignKey -> `Membership`
*   `datetime_started`: DateTimeField (Nullable)
*   `datetime_ended`: DateTimeField (Nullable)

---

## 7. Address App (`address`)

### `Country`
*   `id`: AutoField (PK)
*   `name`: CharField

### `Province`
*   `id`: AutoField (PK)
*   `country`: ForeignKey -> `Country`
*   `name`: CharField

### `RegencyMunicipality`
*   `id`: AutoField (PK)
*   `province`: ForeignKey -> `Province`
*   `name`: CharField

### `District`
*   `id`: AutoField (PK)
*   `regency_municipality`: ForeignKey -> `RegencyMunicipality`
*   `name`: CharField

### `Village`
*   `id`: AutoField (PK)
*   `district`: ForeignKey -> `District`
*   `name`: CharField
*   `post_code`: CharField

### `Street`
*   `id`: AutoField (PK)
*   `name`: CharField

### `UserAddress`
*   `id`: AutoField (PK)
*   `user`: ForeignKey -> `user.User` (Nullable)
*   `receiver_name`: CharField
*   `receiver_phone_number`: CharField
*   `street`: ForeignKey -> `Street`
*   `lattitude`: DecimalField(9,6) (Nullable)
*   `longitude`: DecimalField(9,6) (Nullable)
*   `other_details`: TextField (Nullable)
*   `is_main_address`: BooleanField (Default: False)
*   `is_office`: BooleanField (Default: False)
*   `datetime_added`: DateTimeField (auto_now_add=True)
*   `datetime_last_updated`: DateTimeField (auto_now=True)

---

## 8. Voucher App (`voucher`)

### `VoucherOrder`
*   `id`: AutoField (PK)
*   `name`: CharField
*   `source_type`: CharField (Choices: Code, Offer, Membership Reward, Point Redeem)
*   `description`: TextField (Nullable)
*   `img_url`: URLField (Nullable)
*   `min_item_quantity`: PositiveIntegerField
*   `min_item_cost`: DecimalField(12,2)
*   `discount_precentage`: DecimalField(8,2)
*   `max_nominal_discount`: DecimalField(12,2) (Nullable)
*   `datetime_added`: DateTimeField (auto_now_add=True)
*   `datetime_last_updated`: DateTimeField (auto_now=True)
*   `datetime_started`: DateTimeField (Nullable)
*   `datetime_expiry`: DateTimeField (Nullable)

### `VoucherOrderCode`
*   `id`: AutoField (PK)
*   `voucher_order`: OneToOneField -> `VoucherOrder`
*   `code`: CharField (Unique)
*   `datetime_started`: DateTimeField (Nullable)
*   `datetime_ended`: DateTimeField (Nullable)

### `UserVoucherOrder`
*   `id`: AutoField (PK)
*   `user`: ForeignKey -> `user.User`
*   `voucher_order`: ForeignKey -> `VoucherOrder`
*   `is_used`: BooleanField (Default: False)
*   `datetime_added`: DateTimeField (auto_now_add=True)

---

## 9. Point App (`point`)

### `NetflixDiscountPointReedem`
*   `id`: AutoField (PK)
*   `name`: CharField
*   `description`: TextField (Nullable)
*   `point_required`: PositiveIntegerField
*   `min_membership`: ForeignKey -> `membership.Membership` (Nullable)
*   `netflix_discount_id`: CharField
*   `min_movie_cost`: DecimalField(12,2)
*   `discount_precentage`: DecimalField(8,2)
*   `max_nominal_discount`: DecimalField(12,2) (Nullable)
*   `datetime_started`: DateTimeField (auto_now_add=True)

### `UserNetflixDiscountPointReedem`
*   `id`: AutoField (PK)
*   `user`: ForeignKey -> `user.User`
*   `netflix_discount_reedem`: ForeignKey -> `NetflixDiscountPointReedem`
*   `datetime_added`: DateTimeField (auto_now_add=True)
*   `datetime_reedem`: DateTimeField (Nullable)

### `VoucherOrderPointReedem`
*   `id`: AutoField (PK)
*   `voucher_order`: OneToOneField -> `voucher.VoucherOrder`
*   `point_required`: PositiveIntegerField
*   `min_membership`: ForeignKey -> `membership.Membership` (Nullable)
*   `datetime_started`: DateTimeField (auto_now_add=True)

---

## 10. Payment App (`payment`)

### `PaymentMethod`
*   `id`: AutoField (PK)
*   `name`: CharField
*   `fee`: DecimalField(12,2)
*   `discount`: DecimalField(12,2)
*   `datetime_added`: DateTimeField (auto_now_add=True)
*   `datetime_last_updated`: DateTimeField (auto_now=True)

### `UserPaymentMethod`
*   `id`: AutoField (PK)
*   `user`: ForeignKey -> `user.User`
*   `payment_method`: ForeignKey -> `PaymentMethod`
*   `account_number`: CharField
*   `token`: CharField (Nullable)
*   `datetime_added`: DateTimeField (auto_now_add=True)

### `UserTopupWalletBalancePayment`
*   `id`: AutoField (PK)
*   `topup_wallet_balance`: ForeignKey -> `wallet.UserTopupWalletBalance`
*   `payment_method`: ForeignKey -> `PaymentMethod`
*   `account_number`: CharField
*   `status`: CharField (Default: 'pending')
*   `datetime_created`: DateTimeField (auto_now_add=True)
*   `datetime_finished`: DateTimeField (Nullable)

### `OrderPayment`
*   `id`: AutoField (PK)
*   `order`: ForeignKey -> `order.Order`
*   `payment_method`: ForeignKey -> `PaymentMethod` (Nullable)
*   `account_number`: CharField
*   `user_voucher_order`: ForeignKey -> `voucher.UserVoucherOrder` (Nullable)
*   `status`: CharField (Default: 'pending')
*   `datetime_created`: DateTimeField (auto_now_add=True)
*   `datetime_finished`: DateTimeField (Nullable)
