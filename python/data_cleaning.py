"""
Blinkit Grocery Sales Analysis
Step 1: Data quality checks and cleaning.

Run from the project root:
    python python/data_cleaning.py
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = ROOT / "data" / "raw" / "BlinkIT-Grocery-Data.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "blinkit_cleaned.csv"

def main():
    df = pd.read_csv(RAW_FILE)

    print("\n--- INITIAL DATASET ---")
    print(f"Shape: {df.shape}")
    print("\nData types:")
    print(df.dtypes)
    print("\nMissing values:")
    print(df.isna().sum())
    print(f"\nDuplicate rows: {df.duplicated().sum()}")

    # Standardize category labels without discarding valid records.
    df["Item Fat Content"] = (
        df["Item Fat Content"].astype("string").str.strip().str.lower()
        .replace({
            "lf": "low fat",
            "low fat": "low fat",
            "reg": "regular",
            "regular": "regular",
        })
        .map({"low fat": "Low Fat", "regular": "Regular"})
    )

    # Recover missing weights from other rows for the same product.
    # The dataset has repeated products across outlets. The product identifier
    # is the grouping key; median is robust if multiple values are present.
    missing_weight_before = int(df["Item Weight"].isna().sum())
    product_weight = df.groupby("Item Identifier")["Item Weight"].transform("median")
    df["Item Weight"] = df["Item Weight"].fillna(product_weight)
    missing_weight_after_product_fill = int(df["Item Weight"].isna().sum())

    # If any values remain missing (a product has no observed weight anywhere),
    # fill with the median for that product category as a documented fallback.
    category_weight_median = df.groupby("Item Type")["Item Weight"].transform("median")
    df["Item Weight"] = df["Item Weight"].fillna(category_weight_median)
    missing_weight_after = int(df["Item Weight"].isna().sum())

    # Keep the original source intact; write a separate processed file.
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print("\n--- CLEANING SUMMARY ---")
    print(f"Rows/columns retained: {df.shape}")
    print(f"Item Weight missing before: {missing_weight_before}")
    print(f"Missing after product-level fill: {missing_weight_after_product_fill}")
    print(f"Missing after category fallback: {missing_weight_after}")
    print("\nStandardized Item Fat Content:")
    print(df["Item Fat Content"].value_counts(dropna=False))
    print(f"\nSaved cleaned dataset to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
