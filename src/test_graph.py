from data_loader import load_data
from knowledge_graph import create_graph


print("Running graph tests...")

# Load dataset
data = load_data("../data")

# Create graph
graph = create_graph(data)


# ---------------------------------------------------------
# TEST 1: GRAPH EXISTS
# ---------------------------------------------------------

assert graph is not None, "Graph was not created."

print("PASS: Graph was created.")


# ---------------------------------------------------------
# TEST 2: NODE COUNT
# ---------------------------------------------------------

assert graph.number_of_nodes() == 58, (
    f"Expected 58 nodes, got {graph.number_of_nodes()}"
)

print("PASS: Node count is 58.")


# ---------------------------------------------------------
# TEST 3: REQUIRED ENTITY TYPES
# ---------------------------------------------------------

node_types = {
    attributes.get("type")
    for _, attributes in graph.nodes(data=True)
}

required_types = {
    "Product",
    "Brand",
    "Category",
    "Vendor",
    "Customer",
    "Order"
}

assert required_types.issubset(node_types), (
    f"Missing entity types. Found: {node_types}"
)

print("PASS: All required entity types exist.")


# ---------------------------------------------------------
# TEST 4: IMPORTANT NODES
# ---------------------------------------------------------

assert "P001" in graph.nodes, "P001 product is missing."
assert "BR001" in graph.nodes, "BR001 brand is missing."
assert "CAT001" in graph.nodes, "CAT001 category is missing."
assert "V001" in graph.nodes, "V001 vendor is missing."
assert "C001" in graph.nodes, "C001 customer is missing."
assert "O001" in graph.nodes, "O001 order is missing."

print("PASS: Important nodes exist.")


# ---------------------------------------------------------
# TEST 5: IMPORTANT RELATIONSHIPS
# ---------------------------------------------------------

assert graph.has_edge("P001", "BR001"), (
    "P001 -> BR001 relationship is missing."
)

assert graph.has_edge("P001", "CAT001"), (
    "P001 -> CAT001 relationship is missing."
)

assert graph.has_edge("P001", "V001"), (
    "P001 -> V001 relationship is missing."
)

assert graph.has_edge("C001", "O001"), (
    "C001 -> O001 relationship is missing."
)

assert graph.has_edge("O001", "P001"), (
    "O001 -> P001 relationship is missing."
)

print("PASS: Required relationships exist.")


# ---------------------------------------------------------
# TEST 6: BANANA COUNT
# ---------------------------------------------------------

banana_products = []

for node, attributes in graph.nodes(data=True):

    if attributes.get("type") != "Product":
        continue

    product_name = str(attributes.get("name", ""))

    if "banana" in product_name.lower():
        banana_products.append(node)


assert len(banana_products) == 5, (
    f"Expected exactly 5 banana products, "
    f"got {len(banana_products)}: {banana_products}"
)

print("PASS: Exactly 5 banana products exist.")


print("\nAll graph tests passed successfully!")