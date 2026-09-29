# RETRIEVAL LAYER


def get_product_details(graph, product_identifier):
    """
    Retrieve complete details of a product.

    The product can be identified using:
    - Product ID
    - Product name
    """

    if not product_identifier:
        return {
            "error": "No product identifier was provided"
        }

    product_id = None

    for node, attributes in graph.nodes(data=True):

        if attributes.get("type") != "Product":
            continue

        # Match product ID
        if str(node).lower() == str(product_identifier).lower():
            product_id = node
            break

        # Match product name
        if (
            str(attributes.get("name", "")).lower()
            == str(product_identifier).lower()
        ):
            product_id = node
            break

    if product_id is None:
        return {
            "error": f"Product '{product_identifier}' not found"
        }

    product = graph.nodes[product_id]

    result = {
        "product_id": product_id,
        "product_name": product.get("name"),
        "price": product.get("price"),
        "brand": None,
        "category": None,
        "vendor": None
    }

    for neighbor in graph.successors(product_id):

        edge_data = graph.get_edge_data(
            product_id,
            neighbor
        )

        for _, data in edge_data.items():

            relation = data.get("relation")

            if relation == "MADE_BY":
                result["brand"] = graph.nodes[neighbor].get("name")

            elif relation == "BELONGS_TO":
                result["category"] = graph.nodes[neighbor].get("name")

            elif relation == "SUPPLIED_BY":
                result["vendor"] = graph.nodes[neighbor].get("name")

    return result


def get_products_by_category(graph, category_name):
    """
    Retrieve all products belonging to a category.
    """

    if not category_name:
        return {
            "error": "No category name was provided"
        }

    products = []

    for node, attributes in graph.nodes(data=True):

        if attributes.get("type") != "Product":
            continue

        for neighbor in graph.successors(node):

            neighbor_data = graph.nodes[neighbor]

            if (
                neighbor_data.get("type") == "Category"
                and str(neighbor_data.get("name", "")).lower()
                == str(category_name).lower()
            ):

                products.append({
                    "product_id": node,
                    "product_name": attributes.get("name"),
                    "price": attributes.get("price")
                })

    return products


def get_products_by_brand_and_vendor(
    graph,
    brand_name,
    vendor_name
):
    """
    Retrieve products that are:
    - made by a specific brand
    - supplied by a specific vendor
    """

    if not brand_name:
        return {
            "error": "No brand name was provided"
        }

    if not vendor_name:
        return {
            "error": "No vendor name was provided"
        }

    products = []

    for node, attributes in graph.nodes(data=True):

        if attributes.get("type") != "Product":
            continue

        found_brand = False
        found_vendor = False

        # Check all outgoing relationships
        for neighbor in graph.successors(node):

            neighbor_data = graph.nodes[neighbor]

            edge_data = graph.get_edge_data(
                node,
                neighbor
            )

            for _, data in edge_data.items():

                relation = data.get("relation")

                # Check brand
                if relation == "MADE_BY":

                    if (
                        str(neighbor_data.get("name", "")).lower()
                        == str(brand_name).lower()
                    ):
                        found_brand = True

                # Check vendor
                elif relation == "SUPPLIED_BY":

                    if (
                        str(neighbor_data.get("name", "")).lower()
                        == str(vendor_name).lower()
                    ):
                        found_vendor = True

        # Product must satisfy BOTH conditions
        if found_brand and found_vendor:

            products.append({
                "product_id": node,
                "product_name": attributes.get("name"),
                "price": attributes.get("price"),
                "brand": brand_name,
                "vendor": vendor_name
            })

    return products


def get_customer_orders(graph, customer_name):
    """
    Retrieve all products ordered by a customer.
    """

    if not customer_name:
        return {
            "error": "No customer name was provided"
        }

    customer_id = None

    for node, attributes in graph.nodes(data=True):

        if (
            attributes.get("type") == "Customer"
            and str(attributes.get("name", "")).lower()
            == str(customer_name).lower()
        ):
            customer_id = node
            break

    if customer_id is None:
        return {
            "error": f"Customer '{customer_name}' not found"
        }

    orders = []

    for order_id in graph.successors(customer_id):

        if graph.nodes[order_id].get("type") != "Order":
            continue

        for product_id in graph.successors(order_id):

            product = graph.nodes[product_id]

            edge_data = graph.get_edge_data(
                order_id,
                product_id
            )

            for _, data in edge_data.items():

                if data.get("relation") == "CONTAINS":

                    orders.append({
                        "order_id": order_id,
                        "product_id": product_id,
                        "product_name": product.get("name"),
                        "quantity": data.get("quantity")
                    })

    return orders


def search_products(graph, search_term):
    """
    Search products by product name.
    """

    if not search_term:
        return {
            "error": "No search term was provided"
        }

    results = []

    search_term = str(search_term).lower()

    for node, attributes in graph.nodes(data=True):

        if attributes.get("type") != "Product":
            continue

        product_name = str(
            attributes.get("name", "")
        )

        if search_term in product_name.lower():

            results.append({
                "product_id": node,
                "product_name": product_name,
                "price": attributes.get("price")
            })

    return results


def get_banana_products(graph):
    """
    Retrieve products containing 'banana' in their name.
    """

    results = []

    for node, attributes in graph.nodes(data=True):

        if attributes.get("type") != "Product":
            continue

        product_name = str(
            attributes.get("name", "")
        )

        if "banana" in product_name.lower():

            results.append({
                "product_id": node,
                "product_name": product_name,
                "price": attributes.get("price")
            })

    return results


def execute_intent(graph, intent):
    """
    Execute the structured intent generated by the LLM.
    """

    if not intent:
        return {
            "error": "No intent was provided"
        }

    operation = intent.get("operation")

    # 1. Product details
    if operation == "product_details":

        product_identifier = (
            intent.get("product_id")
            or intent.get("product_name")
        )

        return get_product_details(
            graph,
            product_identifier
        )

    # 2. Products by category
    elif operation == "products_by_category":

        return get_products_by_category(
            graph,
            intent.get("category")
        )

    # 3. Products by brand and vendor
    elif operation == "products_by_brand_and_vendor":

        return get_products_by_brand_and_vendor(
            graph,
            intent.get("brand")
            or intent.get("brand_name"),
            intent.get("vendor")
            or intent.get("vendor_name")
        )

    # 4. Customer orders
    elif operation == "customer_orders":

        return get_customer_orders(
            graph,
            intent.get("customer_name")
        )

    # 5. Product search
    elif operation == "search_products":

        return search_products(
            graph,
            intent.get("search_term")
        )

    # 6. Banana products
    elif operation == "banana_products":

        return get_banana_products(graph)

    # Unknown operation
    else:

        return {
            "error": f"Unknown operation: {operation}"
        }