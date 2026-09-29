import pandas as pd
from pathlib import Path


def load_data(data_dir):
    data_dir = Path(data_dir)

    products = pd.read_csv(data_dir / "products.csv")
    brands = pd.read_csv(data_dir / "brands.csv")
    categories = pd.read_csv(data_dir / "categories.csv")
    vendors = pd.read_csv(data_dir / "vendors.csv")
    customers = pd.read_csv(data_dir / "customers.csv")
    orders = pd.read_csv(data_dir / "orders.csv")

    return {
        "products": products,
        "brands": brands,
        "categories": categories,
        "vendors": vendors,
        "customers": customers,
        "orders": orders,
    }