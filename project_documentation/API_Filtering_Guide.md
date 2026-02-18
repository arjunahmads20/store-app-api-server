# Product and Order Filtering, Search, and Sorting Guide

This section details the **Advanced Filtering, Search, and Sorting capabilities** available for the Product API (`/api/v1/product/products/` and `/api/v1/product/product-in-stores/`) and Order API (`/api/v1/order/orders/`).

The filters are implemented using `DjangoFilterBackend` but include custom logic for stock, promotions, and recommendations.

## 1. Product Filtering

### 1.1 Basic Filtering

| Parameter | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `min_price` | Number | Filter products with `sell_price >= value`. | `?min_price=1000` |
| `max_price` | Number | Filter products with `sell_price <= value`. | `?max_price=5000` |
| `category` | Integer | Exact match on Category ID. | `?category=3` |
| `category_name` | String | Case-insensitive match on Category Name. | `?category_name=electronics` |
| `tags` | String | Case-insensitive match on Tags. | `?tags=organic` |
| `store` | Integer | Exact match on Store ID. | `?store=1` |

---

### 1.2 Service Flags & Stock

| Parameter | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `is_in_stock` | Boolean | If `true`, returns only products with `stock > 0`. | `?is_in_stock=true` |
| `is_support_cod` | Boolean | Filter by Cash on Delivery support. | `?is_support_cod=true` |
| `is_support_instant_delivery` | Boolean | Filter by Instant Delivery support. | `?is_support_instant_delivery=true` |

---

### 1.3 Promotions (Discounts & Flashsales)
All promotion filters automatically validate against the **Current Time** (`now`). Expired promotions are excluded.

| Parameter | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `is_in_discount` | Boolean | If `true`, returns products with an **active** discount. | `?is_in_discount=true` |
| `discount_id` | Integer | Filter by specific Discount Campaign ID. | `?discount_id=5` |
| `discount_label` | String | Search by Discount Label (e.g., "Summer Sale"). | `?discount_label=summer` |
| `is_in_flashsale` | Boolean | If `true`, returns products in an **active** flashsale. | `?is_in_flashsale=true` |
| `flashsale_id` | Integer | Filter by specific Flashsale Event ID. | `?flashsale_id=2` |
| `is_contain_points` | Boolean | If `true`, returns products that earn Points. | `?is_contain_points=true` |

---

### 1.4 Recommendations (Intelligent Sorting)
The recommendation engine personalizes results based on user behavior.

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `is_recommended` | Boolean | If `true`, activates the scoring engine. |

**How it works:**
1.  **Authenticated Users**:
    *   Analyzes the user's **Latest Order**.
    *   extracts **Tags** from purchased items.
    *   Finds matching products in the catalog.
    *   **Sorts by Similarity Score** (number of matching tags).
    *   *Fallback*: If no history, defaults to Best Sellers.
2.  **Guests / Anonymous**:
    *   Returns **Best Sellers** (Sorted by `-sold_count`).

---

## 2. Product Search
The search function is a "Fuzzy Search" that queries multiple fields simultaneously.

| Parameter | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `search_keyword` | String | Searches `name`, `category_name`, `description`, and `tags`. | `?search_keyword=iphone` |

---

## 3. Product Sorting
Sort results using the `?sortby` parameter. Use a hyphen `-` for descending order.

| Resource | Available Sort Keys | Example |
| :--- | :--- | :--- |
| **Products** | `name`, `sell_price`, `sold_count`, `category_name`, `datetime_added` | `?sortby=sell_price` |

---

## 4. Order Filtering

| Parameter | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `status` | String | Filter by Order Status. | `?status=pending` |
| `payment_method` | Integer | Filter by Payment Method ID. | `?payment_method=1` |
| `payment_method_name` | String | Filter by Payment Method Name (Fuzzy). | `?payment_method_name=OVO` |
| `store` | Integer | Filter by Store ID. | `?store=5` |
| `delivery_type` | Integer | Filter by Delivery Type ID. | `?delivery_type=2` |

---

## 5. Order Sorting

| Resource | Available Sort Keys | Example |
| :--- | :--- | :--- |
| **Orders** | `datetime_created`, `status` | `?sortby=-datetime_created` |
