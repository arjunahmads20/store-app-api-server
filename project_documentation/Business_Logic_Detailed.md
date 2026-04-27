# Business Logic Documentation

This document describes the key business rules and algorithms implemented in the Store API Server.

## 1. Authentication & User Management

### 1.1. Registration & Referrals
*   **Endpoint**: `POST /api/v1/users/signup/`
*   **Logic**:
    1.  User submits basic info and optional `referral_code`.
    2.  System validates unique Phone Number.
    3.  If `referral_code` is present:
        *   System looks up the referrer's `UserMembership`.
        *   Finds an **Active Invitation Rule** (based on current date).
        *   Creates a `UserInvitation` linking the new user, the referrer, and the active rule.
    4.  Auth Token is returned immediately.

### 1.2. Invitation Rewards (First Login)
*   **Endpoint**: `POST /api/v1/users/login/`
*   **Trigger**: First successful login (`datetime_last_login` is NULL).
*   **Logic**:
    1.  Check for pending `UserInvitation` for this user.
    2.  If found and linked to an `InvitationRule`:
        *   **Inviter Reward**: Add `point_earned_by_inviter` to referrer's `UserMembership` points.
        *   **Invitee Reward**: Add `point_earned_by_invitee` to new user's points (if applicable).
    3.  Update `datetime_last_login` to ensure this only happens once.

### 1.3. Authorization
*   **Permissions**:
    *   `AllowAny`: Signup, Login, Public Catalog.
    *   `IsAuthenticated`: Most endpoints.
    *   `IsOwner`: Custom permission ensuring users can only access/edit their own data (Orders, Addresses, Profile).
    *   `IsStaff` (Admin): Full access to resources.
*   **Token**: All secured requests must include header `Authorization: Token <token>`.

---

## 2. Product & Catalog

### 2.1. Recommendation Engine (Tag-Based)
*   **Endpoint**: `GET /api/v1/products/products/?is_recommended=true`
*   **Algorithm**: "Tag Intersection Sorting"
    1.  **History Fetch**: Retrieve user's **latest** `Order`.
    2.  **Tag Extraction**: Collect all tags from products in that order.
    3.  **Candidate Scoring**:
        *   For every available product, calculate **Score** = Count of tags overlapping with User's extracted tags.
    4.  **Ranking**: Sort products by Score (Descending).
    5.  **Fallback**: If user has no history or zero matches found, return **Best Sellers** (`sold_count` descending).

### 2.2. Advanced Filtering
*   **Custom Pagination**: `?page=<page_num>,<limit>` (e.g., `?page=1,20`).
*   **Search**: Searches across Name, Category, Description, and Tags.
*   **Flags**: `is_in_stock` (stock > 0), `is_in_discount` (active discount), `is_in_flashsale`.

---

## 3. Order Processing

### 3.1. Checkout Validation
*   **Endpoint**: `POST /api/v1/orders/orders/checkout/`
*   **Purpose**: Pre-flight check before creating an order.
*   **Checks**:
    1.  **Active Order**: User cannot have another `pending` or `processed` order.
    2.  **Empty Cart**: Must have items checked (`is_checked=True`) in `UserCart`.
    3.  **Daily Quota**: Total items cannot exceed User's `daily_product_quota`.
    4.  **Stock Availability**: All items must exist in the selected `Store` with sufficient `stock`.
    5.  **Voucher Validity**:
        *   Start/Expiry Date check.
        *   `min_item_quantity` met.
        *   `min_item_cost` met.
        *   Unused check (`is_used=False`).

### 3.2. Order Creation Policy
*   **Endpoint**: `POST /api/v1/orders/orders/`
*   **Transaction**: ACID transaction guarantees consistency.
*   **Steps**:
    1.  **Re-Validation**: Runs all checkout checks again (Stock, Quota, Voucher).
    2.  **Inventory Update**: Deducts `stock` from `ProductInStore`.
    3.  **Flashsale Update**: Decrements flashsale stock/quota if applicable.
    4.  **Point Calculation**: Aggregates points from `ProductInStorePoint` rules.
    5.  **Order Record**: Creates `Order` and `ProductInOrder` lines.
    6.  **Quota Deduction**: Updates User's `daily_product_quota`.
    7.  **Voucher Consumption**: Marks `UserVoucherOrder` as `is_used=True`.
    8.  **Point Awarding**: Adds calculated points to `UserMembership`.
    9.  **Payment Record**: Initializes `OrderPayment` with status `pending`.

---

## 4. Address Management

### 4.1. Main Address Logic
*   **Constraint**: A user can have only **one** `is_main_address=True`.
*   **Logic**:
    *   On Create/Update: If `is_main_address` is set to `True`, the system automatically updates all *other* addresses for that user to `False`.

### 4.2. Ownership
*   Strict `IsOwner` enforcement prevents manipulating other users' addresses, even if ID is guessed.

---

## 5. Naming & Formatting Standards

*   **Code**: Python `snake_case` for variables, functions. `PascalCase` for Classes/Models.
*   **API Fields**: `snake_case` (JSON).
    *   Check: `datetime_created` (not `createdAt`), `phone_number`.
*   **Database**: Standard Django naming (e.g., `user_id` FK).
