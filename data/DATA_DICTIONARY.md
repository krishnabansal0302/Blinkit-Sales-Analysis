# Data dictionary

Source: `raw/BlinkIT-Grocery-Data.csv`; cleaned output: `processed/blinkit_cleaned.csv`.

| Column | Meaning / use | Type |
|---|---|---|
| Item Fat Content | Product fat-content classification; standardized to Low Fat / Regular | Text |
| Item Identifier | Product identifier | Text |
| Item Type | Product category | Text |
| Outlet Establishment Year | Year outlet was established | Whole number |
| Outlet Identifier | Outlet identifier | Text |
| Outlet Location Type | Location tier (Tier 1/2/3) | Text |
| Outlet Size | Outlet size category | Text |
| Outlet Type | Outlet format | Text |
| Item Visibility | Item visibility metric in the source dataset | Decimal |
| Item Weight | Item weight; missing values imputed during cleaning | Decimal |
| Sales | Sales measure supplied by source | Decimal |
| Rating | Rating measure supplied by source | Decimal |

## Important limitations
The source has no transaction date, order ID, quantity/units sold, cost or profit columns. Do not infer sales growth over time, average order value, units sold, margin or profit. The establishment year describes an outlet attribute, not the date of a sale. Visibility analyses are descriptive associations only.
