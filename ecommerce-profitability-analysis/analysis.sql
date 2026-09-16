-- ============================================================
-- E-Commerce Profitability Analysis
-- Schema: OrderID, Month, Quarter, State, CustomerName,
--         Category, SubCategory, PaymentMode, Quantity, Amount, Profit
-- ============================================================

-- 1. CUSTOMER-LEVEL RFM SEGMENTATION
WITH customer_agg AS (
    SELECT
        CustomerName,
        COUNT(DISTINCT OrderID) AS frequency,
        SUM(Amount)             AS monetary,
        SUM(Profit)             AS total_profit
    FROM ecommerce_data
    GROUP BY CustomerName
),
rfm_scored AS (
    SELECT
        CustomerName, frequency, monetary, total_profit,
        NTILE(4) OVER (ORDER BY frequency   ASC) AS f_score,
        NTILE(4) OVER (ORDER BY monetary    ASC) AS m_score,
        NTILE(4) OVER (ORDER BY total_profit ASC) AS p_score
    FROM customer_agg
)
SELECT
    CustomerName, frequency, monetary, total_profit,
    f_score, m_score, p_score,
    (f_score + m_score + p_score) AS rfm_total,
    CASE
        WHEN f_score >= 3 AND m_score >= 3 AND p_score >= 3 THEN 'Champion'
        WHEN f_score >= 3 AND m_score >= 3 THEN 'Loyal'
        WHEN p_score <= 2 AND m_score >= 3 THEN 'At Risk (High Value, Low Profit)'
        ELSE 'Hibernating'
    END AS customer_segment
FROM rfm_scored
ORDER BY rfm_total DESC;


-- 2. STATE-LEVEL PROFITABILITY RANKING
WITH state_metrics AS (
    SELECT
        State,
        SUM(Amount)   AS total_sales,
        SUM(Profit)   AS total_profit,
        SUM(Quantity) AS total_quantity,
        ROUND(100.0 * SUM(Profit) / NULLIF(SUM(Amount), 0), 2) AS profit_margin_pct
    FROM ecommerce_data
    GROUP BY State
)
SELECT
    State, total_sales, total_profit, total_quantity, profit_margin_pct,
    DENSE_RANK() OVER (ORDER BY total_profit DESC) AS profit_rank,
    CASE
        WHEN total_profit < 0 THEN 'Loss-Making Region'
        WHEN profit_margin_pct < 5 THEN 'Low Margin'
        ELSE 'Healthy'
    END AS region_health
FROM state_metrics
ORDER BY profit_rank;


-- 3. PAYMENT MODE RISK ANALYSIS
WITH payment_metrics AS (
    SELECT
        PaymentMode,
        COUNT(DISTINCT OrderID) AS order_count,
        SUM(Amount) AS total_sales,
        SUM(Profit) AS total_profit
    FROM ecommerce_data
    GROUP BY PaymentMode
)
SELECT
    PaymentMode, order_count,
    ROUND(100.0 * order_count / (SELECT COUNT(DISTINCT OrderID) FROM ecommerce_data), 2) AS pct_of_orders,
    total_sales, total_profit,
    ROUND(100.0 * total_profit / NULLIF(total_sales, 0), 2) AS profit_margin_pct,
    ROUND(100.0 * total_profit / NULLIF(SUM(total_profit) OVER (), 0), 2) AS pct_of_total_profit
FROM payment_metrics
ORDER BY total_profit ASC;


-- 4. CATEGORY & SUB-CATEGORY PROFIT CONCENTRATION
WITH subcat_metrics AS (
    SELECT
        Category, SubCategory,
        SUM(Quantity) AS units_sold,
        SUM(Amount)   AS revenue,
        SUM(Profit)   AS profit
    FROM ecommerce_data
    GROUP BY Category, SubCategory
)
SELECT
    Category, SubCategory, units_sold, revenue, profit,
    ROUND(100.0 * units_sold / SUM(units_sold) OVER (), 2) AS pct_of_units,
    ROUND(100.0 * profit / NULLIF(SUM(profit) OVER (), 0), 2) AS pct_of_total_profit,
    SUM(profit) OVER (PARTITION BY Category ORDER BY profit DESC) AS running_profit_in_category
FROM subcat_metrics
ORDER BY profit DESC;