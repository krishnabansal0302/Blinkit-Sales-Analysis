-- Blinkit Grocery Sales Analysis (MySQL 8+)
-- Import data/processed/blinkit_cleaned.csv into a table named blinkit_sales.
-- Suggested column names below use snake_case for SQL convenience.

-- 1. Overall business KPIs
SELECT
    COUNT(*) AS record_count,
    COUNT(DISTINCT `Item Identifier`) AS unique_products,
    COUNT(DISTINCT `Outlet Identifier`) AS unique_outlets,
    ROUND(SUM(`Sales`), 2) AS total_sales,
    ROUND(AVG(`Sales`), 2) AS average_sales_per_record,
    ROUND(AVG(`Rating`), 2) AS average_rating
FROM blinkit_sales;

-- 2. Sales by product category
SELECT `Item Type`, ROUND(SUM(`Sales`), 2) AS total_sales,
       ROUND(AVG(`Sales`), 2) AS avg_sales, COUNT(*) AS record_count
FROM blinkit_sales
GROUP BY `Item Type`
ORDER BY total_sales DESC;

-- 3. Sales by outlet type
SELECT `Outlet Type`, ROUND(SUM(`Sales`), 2) AS total_sales,
       ROUND(AVG(`Sales`), 2) AS avg_sales, COUNT(*) AS record_count
FROM blinkit_sales
GROUP BY `Outlet Type`
ORDER BY total_sales DESC;

-- 4. Sales by location tier
SELECT `Outlet Location Type`, ROUND(SUM(`Sales`), 2) AS total_sales,
       ROUND(AVG(`Sales`), 2) AS avg_sales
FROM blinkit_sales
GROUP BY `Outlet Location Type`
ORDER BY total_sales DESC;

-- 5. Fat-content performance
SELECT `Item Fat Content`, ROUND(SUM(`Sales`), 2) AS total_sales,
       ROUND(AVG(`Sales`), 2) AS avg_sales, COUNT(*) AS record_count
FROM blinkit_sales
GROUP BY `Item Fat Content`
ORDER BY total_sales DESC;

-- 6. Outlet size comparison
SELECT `Outlet Size`, ROUND(SUM(`Sales`), 2) AS total_sales,
       ROUND(AVG(`Sales`), 2) AS avg_sales
FROM blinkit_sales
GROUP BY `Outlet Size`
ORDER BY total_sales DESC;

-- 7. Top 10 products by total sales
SELECT `Item Identifier`, `Item Type`, ROUND(SUM(`Sales`), 2) AS total_sales
FROM blinkit_sales
GROUP BY `Item Identifier`, `Item Type`
ORDER BY total_sales DESC
LIMIT 10;

-- 8. Bottom 10 product categories by total sales
SELECT `Item Type`, ROUND(SUM(`Sales`), 2) AS total_sales
FROM blinkit_sales
GROUP BY `Item Type`
ORDER BY total_sales ASC
LIMIT 10;

-- 9. Average rating by outlet type
SELECT `Outlet Type`, ROUND(AVG(`Rating`), 2) AS average_rating
FROM blinkit_sales
GROUP BY `Outlet Type`
ORDER BY average_rating DESC;

-- 10. Outlet establishment cohort comparison
SELECT `Outlet Establishment Year`,
       ROUND(SUM(`Sales`), 2) AS total_sales,
       ROUND(AVG(`Sales`), 2) AS average_sales
FROM blinkit_sales
GROUP BY `Outlet Establishment Year`
ORDER BY `Outlet Establishment Year`;

-- 11. Item visibility and sales (descriptive association, not causation)
SELECT
    CASE
        WHEN `Item Visibility` < 0.05 THEN 'Low visibility'
        WHEN `Item Visibility` < 0.15 THEN 'Medium visibility'
        ELSE 'High visibility'
    END AS visibility_band,
    ROUND(AVG(`Sales`), 2) AS average_sales,
    COUNT(*) AS record_count
FROM blinkit_sales
GROUP BY visibility_band
ORDER BY average_sales DESC;

-- 12. Rank item categories by sales using a window function
WITH category_sales AS (
    SELECT `Item Type`, SUM(`Sales`) AS total_sales
    FROM blinkit_sales
    GROUP BY `Item Type`
)
SELECT `Item Type`, ROUND(total_sales, 2) AS total_sales,
       DENSE_RANK() OVER (ORDER BY total_sales DESC) AS sales_rank
FROM category_sales
ORDER BY sales_rank;

-- 13. High-rated outlet types
SELECT `Outlet Type`, ROUND(AVG(`Rating`), 2) AS average_rating,
       COUNT(*) AS record_count
FROM blinkit_sales
GROUP BY `Outlet Type`
HAVING AVG(`Rating`) >= 4
ORDER BY average_rating DESC;

-- 14. Compare average sales for low-fat vs regular items by outlet type
SELECT `Outlet Type`, `Item Fat Content`,
       ROUND(AVG(`Sales`), 2) AS average_sales
FROM blinkit_sales
GROUP BY `Outlet Type`, `Item Fat Content`
ORDER BY `Outlet Type`, `Item Fat Content`;

-- 15. Sales contribution percentage by outlet type
WITH outlet_sales AS (
    SELECT `Outlet Type`, SUM(`Sales`) AS total_sales
    FROM blinkit_sales
    GROUP BY `Outlet Type`
)
SELECT `Outlet Type`, ROUND(total_sales, 2) AS total_sales,
       ROUND(100 * total_sales / SUM(total_sales) OVER (), 2) AS sales_pct
FROM outlet_sales
ORDER BY total_sales DESC;
