import networkx as nx


def create_graph(data):

    graph = nx.MultiDiGraph()

    # ==========================================
    # 1. CREATE PRODUCT NODES
    # ==========================================

    for _, row in data["products"].iterrows():

        graph.add_node(
            row["product_id"],
            type="Product",
            name=row["product_name"],
            price=row["price"]
        )

    # ==========================================
    # 2. CREATE BRAND NODES
    # ==========================================

    for _, row in data["brands"].iterrows():

        graph.add_node(
            row["brand_id"],
            type="Brand",
            name=row["brand_name"]
        )

    # ==========================================
    # 3. CREATE CATEGORY NODES
    # ==========================================

    for _, row in data["categories"].iterrows():

        graph.add_node(
            row["category_id"],
            type="Category",
            name=row["category_name"]
        )

    # ==========================================
    # 4. CREATE VENDOR NODES
    # ==========================================

    for _, row in data["vendors"].iterrows():

        graph.add_node(
            row["vendor_id"],
            type="Vendor",
            name=row["vendor_name"],
            city=row["city"]
        )

    # ==========================================
    # 5. CREATE CUSTOMER NODES
    # ==========================================

    for _, row in data["customers"].iterrows():

        graph.add_node(
            row["customer_id"],
            type="Customer",
            name=row["customer_name"],
            city=row["city"]
        )

    # ==========================================
    # 6. CREATE ORDER NODES
    # ==========================================

    for _, row in data["orders"].iterrows():

        graph.add_node(
            row["order_id"],
            type="Order"
        )

    # ==========================================
    # 7. PRODUCT → BRAND
    # ==========================================

    for _, row in data["products"].iterrows():

        graph.add_edge(
            row["product_id"],
            row["brand_id"],
            relation="MADE_BY"
        )

    # ==========================================
    # 8. PRODUCT → CATEGORY
    # ==========================================

    for _, row in data["products"].iterrows():

        graph.add_edge(
            row["product_id"],
            row["category_id"],
            relation="BELONGS_TO"
        )

    # ==========================================
    # 9. PRODUCT → VENDOR
    # ==========================================

    for _, row in data["products"].iterrows():

        graph.add_edge(
            row["product_id"],
            row["vendor_id"],
            relation="SUPPLIED_BY"
        )

    # ==========================================
    # 10. CUSTOMER → ORDER
    # ==========================================

    for _, row in data["orders"].iterrows():

        graph.add_edge(
            row["customer_id"],
            row["order_id"],
            relation="PLACED"
        )

    # ==========================================
    # 11. ORDER → PRODUCT
    # ==========================================

    for _, row in data["orders"].iterrows():

        graph.add_edge(
            row["order_id"],
            row["product_id"],
            relation="CONTAINS",
            quantity=row["quantity"]
        )

    return graph