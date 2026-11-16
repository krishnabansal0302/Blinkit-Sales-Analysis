# Blinkit sales analysis — summary

## Dataset and quality
- 8,523 records and 12 columns.
- 1,559 distinct item identifiers and 10 distinct outlets.
- 1,463 missing item weights in the raw data; 1,459 were filled using the median weight for the same item identifier, and the remaining 4 using the median for the corresponding item type.
- No duplicate rows detected in the raw data.
- Fat-content labels standardized to `Low Fat` (5,517 records) and `Regular` (3,006 records).
- No missing values remain in the cleaned output.

## Overall KPIs
| KPI | Value |
|---|---:|
| Total Sales | 1,201,681.49 |
| Average Sales per Dataset Record | 140.99 |
| Average Rating | 3.97 |
| Records | 8,523 |
| Unique Products | 1,559 |
| Unique Outlets | 10 |

## Selected descriptive findings
- Fruits and Vegetables has the highest category total (178,124.08), narrowly ahead of Snack Foods (175,433.92).
- Supermarket Type1 has the highest outlet-format total (787,549.89).
- Tier 3 has the highest location-tier total (472,133.03), followed by Tier 2 (393,150.65) and Tier 1 (336,397.81).
- Low Fat items contribute 776,319.69 in total sales; Regular items contribute 425,361.80.
- Medium outlets contribute 507,895.74; Small outlets 444,794.17; High outlets 248,991.59.

## Interpretation caution
These are sums of the dataset's `Sales` field, not profit. The file contains no transaction dates, order identifiers, units, costs or profit. Therefore the analysis does not support time-series sales trends, average order value, units sold, profit/margin or causal claims.
