# Store API Server - Setup Walkthrough

## Overview
Successfully initialized the **Store API Server** using Django and Django REST Framework. The project uses a **fully modular architecture** with **Store-specific inventory logic**.

## Project Structure
The project has been split into 10 apps:

-   **`store`**: `api/v1/stores/`
-   **`product`**: `api/v1/products/` (Includes `store-products`, `store-carts`)
-   **`user`**: `api/v1/users/`
-   **`order`**: `api/v1/orders/`
-   **`wallet`**: `api/v1/wallets/`
-   **`payment`**: `api/v1/paments/`
-   **`voucher`**: `api/v1/vouchers/`
-   **`membership`**: `api/v1/memberships/`
-   **`address`**: `api/v1/addresses/`
-   **`point`**: `api/v1/points/`

## Verification Results
### Database Migrations
All models, including the complex refactor for `ProductInStore`, have been successfully migrated.

### API Status
The server is exposing standard CRUD endpoints.
-   Users can be assigned to a Store (`id_store_work_on`).
-   Inventory is managed via `store-products` endpoint.
-   Orders are linked to specific Stores and Cashiers.

```bash
# Start the server
python manage.py runserver
```

## Data Setup
### Admin Panel
All models have been registered on the Django Admin panel.

### Sample Data
The database has been populated with comprehensive sample data using `store/management/commands/populate_data.py`. This includes:
- **Core**: 15 Users, 1 Admin, 1 Store
- **Inventory**: >20 Products, Categories, Stock, Flashsales, Discounts
- **Orders**: >15 Orders (various statuses), Deliveries, Payments, Reviews
- **Features**: Wallets (Topups/Transfers), Memberships (Points/Rewards), Vouchers, Addresses, Favorites, Carts
- **Coverage**: All models have at least one entry, and all fields (including optional ones) are populated.

## Next Steps
-   Populate initial Store and Product data.
-   Test the "Add to Cart" flow with the new `StoreCart` logic.
