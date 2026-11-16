"""
Exploratory data analysis.
Run after data cleaning:
    python python/eda.py
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "processed" / "blinkit_cleaned.csv"
CHART_DIR = ROOT / "reports" / "charts"
SUMMARY_DIR = ROOT / "reports"
CHART_DIR.mkdir(parents=True, exist_ok=True)

def save_bar(series, title, xlabel, ylabel, filename, rotation=0):
    ax = series.plot(kind="bar", figsize=(10, 5))
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=rotation, ha="right")
    plt.tight_layout()
    plt.savefig(CHART_DIR / filename, dpi=160)
    plt.close()

def main():
    df = pd.read_csv(DATA_FILE)

    # Core KPI summary
    kpis = {
        "Total Sales": df["Sales"].sum(),
        "Average Sales per Dataset Row": df["Sales"].mean(),
        "Average Item Rating": df["Rating"].mean(),
        "Number of Records": len(df),
        "Unique Products": df["Item Identifier"].nunique(),
        "Unique Outlets": df["Outlet Identifier"].nunique(),
    }
    pd.Series(kpis, name="Value").to_csv(SUMMARY_DIR / "kpi_summary.csv")

    # Business summaries
    df.groupby("Item Type")["Sales"].agg(
        Total_Sales="sum", Average_Sales="mean", Record_Count="count"
    ).sort_values("Total_Sales", ascending=False).to_csv(SUMMARY_DIR / "sales_by_item_type.csv")

    df.groupby("Outlet Type")["Sales"].agg(
        Total_Sales="sum", Average_Sales="mean", Record_Count="count"
    ).sort_values("Total_Sales", ascending=False).to_csv(SUMMARY_DIR / "sales_by_outlet_type.csv")

    df.groupby("Outlet Location Type")["Sales"].agg(
        Total_Sales="sum", Average_Sales="mean", Record_Count="count"
    ).sort_values("Total_Sales", ascending=False).to_csv(SUMMARY_DIR / "sales_by_location_tier.csv")

    df.groupby("Item Fat Content")["Sales"].agg(
        Total_Sales="sum", Average_Sales="mean", Record_Count="count"
    ).to_csv(SUMMARY_DIR / "sales_by_fat_content.csv")

    # Charts
    save_bar(
        df.groupby("Item Type")["Sales"].sum().sort_values(ascending=False),
        "Total Sales by Item Type", "Item Type", "Sales",
        "sales_by_item_type.png", rotation=65
    )
    save_bar(
        df.groupby("Outlet Type")["Sales"].sum().sort_values(ascending=False),
        "Total Sales by Outlet Type", "Outlet Type", "Sales",
        "sales_by_outlet_type.png", rotation=25
    )
    save_bar(
        df.groupby("Outlet Location Type")["Sales"].sum().sort_index(),
        "Total Sales by Outlet Location Tier", "Location Tier", "Sales",
        "sales_by_location_tier.png"
    )

    print("KPI summary:")
    print(pd.Series(kpis))
    print("\nReports and charts saved in the reports/ folder.")

if __name__ == "__main__":
    main()
