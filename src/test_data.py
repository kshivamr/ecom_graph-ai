from data_loader import load_data

data = load_data("../data")

for name, df in data.items():
    print(f"\n{name}")
    print(df.head())