# Blinkit Sales Analysis & Business Insights

An end-to-end portfolio project exploring the supplied Blinkit grocery outlet dataset with **Python, SQL and Power BI-ready reporting**. The repository also includes a working interactive browser dashboard.

https://krishnabansal0302.github.io/Blinkit-Sales-Analysis/dashboard/

## What is included

- `data/raw/` — original CSV, preserved unchanged.
- `data/processed/blinkit_cleaned.csv` — cleaned dataset (8,523 rows; 12 columns).
- `python/data_cleaning.py` — data-quality checks, category standardization and documented missing-weight imputation.
- `python/eda.py` — KPI calculations, grouped summaries and static charts.
- `sql/business_analysis.sql` — 15 MySQL 8+ business analysis queries using the exact CSV column names.
- `powerbi/DAX_measures.txt` — DAX measures for a native Power BI report.
- `powerbi/BUILD_GUIDE.md` — step-by-step instructions to build and save the `.pbix` in Power BI Desktop.
- `dashboard/index.html` — interactive dashboard with filters for outlet type, location tier, fat content and outlet size. Open it in a browser; internet is required for Plotly charts (loaded from CDN).
- `reports/` — KPI summaries, category/outlet summaries, charts and analysis findings.
- `data/DATA_DICTIONARY.md` — field definitions and analytical limitations.

## Run the Python analysis (Windows PowerShell)

From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python python/data_cleaning.py
python python/eda.py
python build_dashboard.py
```

Open `dashboard/index.html` in Chrome/Edge to use the interactive dashboard.

## SQL setup

Import `data/processed/blinkit_cleaned.csv` into MySQL Workbench. Keep the original column names, create a table named `blinkit_sales`, and run `sql/business_analysis.sql`. The SQL uses backtick-quoted column names matching the CSV headers.

## Native Power BI file

A `.pbix` is a proprietary Power BI Desktop report file. This project contains the cleaned data, DAX measures and detailed report-building guide, but the `.pbix` itself must be saved using Power BI Desktop. Follow `powerbi/BUILD_GUIDE.md` and save it as `powerbi/Blinkit_Sales_Analysis.pbix`.

## Data cleaning decisions

1. Standardize `Item Fat Content`: `LF` and `low fat` become `Low Fat`; `reg` becomes `Regular`.
2. Keep records with missing item weight.
3. Fill missing item weight using the median for the same `Item Identifier` (1,459 values recovered).
4. Fill the remaining 4 missing weights using the median for the corresponding `Item Type`.
5. Preserve the raw source and write a separate processed dataset.

## Validated headline metrics

- Total Sales: 1,201,681.49
- Average Sales per Dataset Record: 140.99
- Average Rating: 3.97
- Records: 8,523
- Unique Products: 1,559
- Unique Outlets: 10

See `reports/analysis_summary.md` for selected findings and `reports/kpi_summary.csv` for the KPI export.

## Analytical limitations

The source contains item/outlet attributes, sales and ratings. It does **not** contain transaction dates, order IDs, units sold, costs or profit. Therefore:
- Do not claim time-series sales trends.
- Do not label `Sales` as profit.
- Do not calculate average order value or units sold.
- Use “average sales per dataset record”, not “average order value”.
- Treat visibility comparisons as descriptive association, not causal evidence.
