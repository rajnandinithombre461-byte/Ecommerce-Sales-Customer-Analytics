"""E-Commerce Sales & Customer Analytics
Run from the project folder: python analyze_ecommerce.py
Uses pandas and matplotlib. The dataset is synthetic and created for portfolio practice.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
data_path = ROOT / "data" / "ecommerce_orders.csv"
output_dir = ROOT / "outputs"
output_dir.mkdir(exist_ok=True)

df = pd.read_csv(data_path, parse_dates=["OrderDate"])
df["Month"] = df["OrderDate"].dt.to_period("M").astype(str)

# Basic data checks
print("Rows:", len(df))
print("Duplicate order IDs:", df["OrderID"].duplicated().sum())
print("Missing values by column:")
print(df.isna().sum().to_string())

# KPI summary
kpis = {
    "Total Orders": df["OrderID"].nunique(),
    "Unique Customers": df["CustomerID"].nunique(),
    "Units Sold": int(df["Quantity"].sum()),
    "Net Sales": round(df["NetSales"].sum(), 2),
    "Total Profit": round(df["Profit"].sum(), 2),
    "Average Order Value": round(df["NetSales"].sum() / df["OrderID"].nunique(), 2),
}
print("\\nKPIs")
for name, value in kpis.items():
    print(f"{name}: {value}")

# Monthly sales trend chart
monthly = df.groupby("Month", as_index=False)["NetSales"].sum()
plt.figure(figsize=(10, 5))
plt.plot(monthly["Month"], monthly["NetSales"], marker="o")
plt.title("Monthly Net Sales")
plt.xlabel("Month")
plt.ylabel("Net Sales")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(output_dir / "monthly_net_sales.png", dpi=150)
plt.close()

# Category sales chart
category = df.groupby("ProductCategory", as_index=False)["NetSales"].sum().sort_values("NetSales")
plt.figure(figsize=(9, 5))
plt.barh(category["ProductCategory"], category["NetSales"])
plt.title("Net Sales by Product Category")
plt.xlabel("Net Sales")
plt.ylabel("Product Category")
plt.tight_layout()
plt.savefig(output_dir / "sales_by_category.png", dpi=150)
plt.close()

# Region profit chart
region = df.groupby("Region", as_index=False)["Profit"].sum().sort_values("Profit")
plt.figure(figsize=(8, 5))
plt.barh(region["Region"], region["Profit"])
plt.title("Profit by Region")
plt.xlabel("Profit")
plt.ylabel("Region")
plt.tight_layout()
plt.savefig(output_dir / "profit_by_region.png", dpi=150)
plt.close()

# Export grouped summaries
df.groupby("ProductCategory", as_index=False).agg(
    Orders=("OrderID", "nunique"),
    UnitsSold=("Quantity", "sum"),
    NetSales=("NetSales", "sum"),
    Profit=("Profit", "sum"),
).to_csv(output_dir / "category_summary.csv", index=False)

print(f"\\nCharts and summary saved in: {output_dir}")
