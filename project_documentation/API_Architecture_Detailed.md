# API Architecture Documentation (Exhaustive)

This document details the architectural standards, conventions, and a **definitive list of every endpoint** exposed by the Store API Server.

## 1. Global Standards

### 1.1. Base URL & Versioning
*   **Prefix**: `/api/v1/`
*   **Versioning Strategy**: Namespace Versioning (currently `v1`).
*   **Format**: `http://<host>:<port>/api/v1/<app-name>/<resource-collection>/`

### 1.2. Naming Conventions
*   **Format**: `snake_case` for all JSON keys and Query Parameters.
*   **IDs**: Uses integer Autofields (e.g., `id`, `user_id`).
*   **Dates**: ISO 8601 strings (e.g., `"2023-01-01T12:00:00Z"`).

### 1.3. Pagination
**Custom Pagination** is enabled globally.
*   **Syntax A**: `?page=<page_number>,<limit>` (e.g., `?page=1,20`).
*   **Syntax B**: `?page=<page_number>&page_size=<limit>` (e.g., `?page=1&page_size=20`).
*   **Response**:
    ```json
    {
        "count": 100,
        "next": "http://.../?page=2,20",
        "previous": null,
        "results": [ ... ]
    }
    ```


### 1.4. Filtering, Searching & Sorting
**Advanced Querying** is supported globally.
*   **Filtering**: Field-based (e.g., `?category=electronics`).
*   **Searching**: Fuzzy search via `?search=<query>`.
*   **Sorting**: Field ordering via `?sortby=<field_name>`.
    *   Ascending: `?sortby=price`
    *   Descending: `?sortby=-price`
    *   Multiple: `?sortby=price,-datetime_added`

---

## 2. Endpoint Reference
*Unless Validation Error (400) or Auth Error (401/403), endpoints return 200/201 on success.*

### 2.1. User App (`/api/v1/user/`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/signup/request-otp/` | Register Step 1: Request OTP. |
| `POST` | `/signup/verify/` | Register Step 2: Verify & Create User. |
| `POST` | `/login/` | Authenticate (Returns Token). |
| `POST` | `/logout/` | Invalidate Token. |
| `CRUD` | `/users/` | User Management. |
| `CRUD` | `/invitation-rules/` | Manage referral point rules. |
| `CRUD` | `/otp-verifications/` | OTP Verification (Forgot Password). |
| **Nested** | | |
| `CRUD` | `/users/{pk}/user-inboxes/` | User's messages. |
| `CRUD` | `/users/{pk}/user-invitations/` | User's sent/received invites. |
| `CRUD` | `/users/{pk}/user-logs/` | User's activity logs. |

### 2.2. Product App (`/api/v1/product/`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `CRUD` | `/product-categories/` | Categories. |
| `CRUD` | `/products/` | **Global Catalog** (Searchable). |
| `CRUD` | `/user-product-favorites/`| User's Wishlist. |
| `CRUD` | `/product-in-stores/` | **Store Inventory** (Main Stock). |
| `CRUD` | `/product-in-store-points/` | Point rules per product. |
| `CRUD` | `/product-in-store-discounts/` | Discount definitions. |
| `CRUD` | `/flashsales/` | Flashsale events. |
| `CRUD` | `/user-carts/` | User Carts (One per user). |
| `CRUD` | `/store-carts/` | Physical Store Carts. |
| **Nested** | | |
| `CRUD` | `/user-carts/{pk}/product-in-user-carts/` | **Items in Cart**. |
| `CRUD` | `/store-carts/{pk}/product-in-store-carts/` | Items in Store Cart. |
| `CRUD` | `/flashsales/{pk}/product-in-store-in-flashsales/` | Items in a Flashsale. |
| `CRUD` | `/product-in-store-discounts/{pk}/product-in-store-in-product-in-store-discounts/` | Active discounts on products. |

### 2.3. Store App (`/api/v1/store/`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `CRUD` | `/stores/` | Physical Store Locations. |

### 2.4. Order App (`/api/v1/order/`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `CRUD` | `/orders/` | **Order Management**. |
| `POST` | `/orders/checkout/` | **Pre-checkout Validation**. |
| `CRUD` | `/delivery-types/` | Shipping Options. |
| `CRUD` | `/product-in-order-reviews/`| Reviews for specific items. |
| **Nested** | | |
| `CRUD` | `/orders/{pk}/product-in-orders/` | Line items in an order. |
| `CRUD` | `/orders/{pk}/order-reviews/` | Review for the order. |

### 2.5. Address App (`/api/v1/address/`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `CRUD` | `/user-addresses/` | User Shipping Addresses. |
| `CRUD` | `/countries/` | Countries. |
| `CRUD` | `/streets/` | Streets. |
| `CRUD` | `/provinces/` | Provinces (Flat List). |
| `CRUD` | `/regency-municipalities/` | Regencies (Flat List). |
| `CRUD` | `/districts/` | Districts (Flat List). |
| `CRUD` | `/villages/` | Villages (Flat List). |
| **Nested** | | **Geo-Hierarchy** |
| `CRUD` | `/countries/{pk}/provinces/` | Provinces in Country. |
| `CRUD` | `.../provinces/{pk}/regency-municipalities/` | Regencies in Province. |
| `CRUD` | `.../regency-municipalities/{pk}/districts/` | Districts in Regency. |
| `CRUD` | `.../districts/{pk}/villages/` | Villages in District. |

### 2.6. Wallet App (`/api/v1/wallet/`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `CRUD` | `/user-wallets/` | User Wallet Info. |
| `CRUD` | `/topup-wallet-balance-rules/` | Top-up Bonus Rules. |
| `CRUD` | `/user-topup-wallet-balances/` | **Top-up Transactions**. |
| `CRUD` | `/user-transfer-wallet-balances/`| **P2P Transfers**. |

### 2.7. Membership App (`/api/v1/membership/`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `CRUD` | `/memberships/` | Tier Definitions. |
| `CRUD` | `/user-memberships/` | User Status. |
| `CRUD` | `/user-membership-histories/` | Log of tier changes. |
| `CRUD` | `/point-membership-rewards/` | Point benefits. |
| `CRUD` | `/user-point-membership-rewards/`| Claimed point rewards. |
| `CRUD` | `/voucher-order-membership-rewards/` | Voucher benefits. |

### 2.8. Payment App (`/api/v1/payment/`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `CRUD` | `/payment-methods/` | System Payment Methods. |
| `CRUD` | `/user-payment-methods/` | User Saved Methods. |
| `CRUD` | `/user-topup-wallet-balance-payments/` | Payments for Top-ups. |
| `CRUD` | `/order-payments/` | Payments for Orders. |

### 2.9. Voucher App (`/api/v1/voucher/`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `CRUD` | `/voucher-orders/` | Voucher Definitions. |
| `CRUD` | `/voucher-order-codes/` | Redeemable Codes. |
| `CRUD` | `/user-voucher-orders/` | **My Vouchers**. |

### 2.10. Point App (`/api/v1/point/`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `CRUD` | `/netflix-discount-point-reedems/`| Netflix Redeem Rules. |
| `CRUD` | `/user-netflix-discount-point-reedems/`| User Redemptions. |
| `CRUD` | `/voucher-order-point-reedems/` | Point-to-Voucher Rules. |

---

## 3. Query Parameter Examples

### Filtering & Sorting
*   `GET /api/v1/product/products/?tags=tech&sortby=-sell_price`
    *   Search for products with 'tech' in tags.
    *   Sort by Price (High to Low).

### Pagination
*   `GET /api/v1/order/orders/?page=1,50` or `GET /api/v1/order/orders/?page=1&page_size=50`
    *   Page 1.
    *   50 Items per page.
