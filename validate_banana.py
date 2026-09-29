from src.data_loader import load_data
from src.knowledge_graph import create_graph


# =========================================================
# LOAD DATA
# =========================================================

data = load_data("data")


# =========================================================
# CREATE KNOWLEDGE GRAPH
# =========================================================

graph = create_graph(data)


# =========================================================
# FIND BANANA PRODUCTS
# =========================================================

banana_products = []

for node, attributes in graph.nodes(data=True):

    # Only check Product nodes
    if attributes.get("type") != "Product":
        continue

    product_name = str(attributes.get("name", ""))

    if "banana" in product_name.lower():

        banana_products.append(
            {
                "node": node,
                "name": product_name
            }
        )


# =========================================================
# DISPLAY RESULTS
# =========================================================

print("Banana products found:")
print()

for product in banana_products:

    print(
        f"{product['node']} -> "
        f"{product['name']}"
    )


# =========================================================
# VALIDATION
# =========================================================

print()
print(
    "Total banana products:",
    len(banana_products)
)


# Exactly 5 banana products are required
assert len(banana_products) == 5, (
    f"Expected exactly 5 banana products, "
    f"but found {len(banana_products)}"
)


# Make sure the expected products are actually present
expected_products = {
    "Banana",
    "Banana Smoothie",
    "Organic Banana",
    "Banana Chips",
    "Banana Bread"
}

actual_products = {
    product["name"]
    for product in banana_products
}

assert actual_products == expected_products, (
    f"Unexpected banana products found: "
    f"{actual_products}"
)


print()
print("SUCCESS: Banana requirement satisfied!")