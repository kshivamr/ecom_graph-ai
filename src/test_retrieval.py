from data_loader import load_data
from knowledge_graph import create_graph

from retrieval import (
    get_product_details,
    get_products_by_category,
    get_products_by_brand_and_vendor,
    get_customer_orders,
    search_products,
    get_banana_products
)


print("Running retrieval tests...")


# =========================================================
# SETUP
# =========================================================

data = load_data("../data")
graph = create_graph(data)


# =========================================================
# TEST 1: PRODUCT DETAILS
# =========================================================

result = get_product_details(
    graph,
    "iPhone 15"
)

assert result["product_id"] == "P001"
assert result["product_name"] == "iPhone 15"
assert result["price"] == 69999
assert result["brand"] == "Apple"
assert result["category"] == "Smartphones"
assert result["vendor"] == "TechWorld"

print("PASS: Product details")


# =========================================================
# TEST 2: PRODUCT NOT FOUND
# =========================================================

result = get_product_details(
    graph,
    "iPhone 16"
)

assert "error" in result

print("PASS: Missing product handled correctly")


# =========================================================
# TEST 3: PRODUCTS BY CATEGORY
# =========================================================

result = get_products_by_category(
    graph,
    "Fruits"
)

product_names = {
    product["product_name"]
    for product in result
}

expected_products = {
    "Banana",
    "Banana Smoothie",
    "Organic Banana",
    "Banana Chips",
    "Banana Bread"
}

assert expected_products.issubset(product_names)

print("PASS: Products by category")


# =========================================================
# TEST 4: BRAND + VENDOR
# =========================================================

result = get_products_by_brand_and_vendor(
    graph,
    "Apple",
    "TechWorld"
)

product_names = {
    product["product_name"]
    for product in result
}

assert "iPhone 15" in product_names
assert "MacBook Air M2" in product_names

assert len(result) == 2

print("PASS: Brand + Vendor retrieval")


# =========================================================
# TEST 5: CUSTOMER ORDERS
# =========================================================

result = get_customer_orders(
    graph,
    "Rahul Sharma"
)

product_names = {
    order["product_name"]
    for order in result
}

assert "iPhone 15" in product_names
assert "Banana" in product_names
assert "MacBook Air M2" in product_names

assert len(result) == 3

print("PASS: Customer orders")


# =========================================================
# TEST 6: PRODUCT SEARCH
# =========================================================

result = search_products(
    graph,
    "mouse"
)

assert len(result) == 1
assert result[0]["product_name"] == "Wireless Mouse"

print("PASS: Product search")


# =========================================================
# TEST 7: BANANA PRODUCTS
# =========================================================

result = get_banana_products(graph)

assert len(result) == 5

banana_names = {
    product["product_name"]
    for product in result
}

expected_banana_products = {
    "Banana",
    "Banana Smoothie",
    "Organic Banana",
    "Banana Chips",
    "Banana Bread"
}

assert banana_names == expected_banana_products

print("PASS: Exactly 5 banana products retrieved")


# =========================================================
# FINAL RESULT
# =========================================================

print()
print("All retrieval tests passed successfully!")