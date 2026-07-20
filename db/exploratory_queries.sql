-- =====================================================
-- NIFTY100 DATABASE - EXPLORATORY SQL QUERIES
-- =====================================================

-- Q1. Total number of companies
SELECT COUNT(*) AS total_companies
FROM companies;


-- Q2. Total rows in Profit & Loss
SELECT COUNT(*) AS total_profit_loss_records
FROM profitandloss;


-- Q3. Top 10 companies by Market Cap
SELECT
    company_id,
    year,
    market_cap_crore
FROM market_cap
ORDER BY market_cap_crore DESC
LIMIT 10;


-- Q4. Top 10 companies by Net Profit
SELECT
    company_id,
    year,
    net_profit
FROM profitandloss
ORDER BY net_profit DESC
LIMIT 10;


-- Q5. Companies with highest ROE
SELECT
    company_id,
    year,
    return_on_equity_pct
FROM financial_ratios
ORDER BY return_on_equity_pct DESC
LIMIT 10;


-- Q6. Number of companies in each sector
SELECT
    broad_sector,
    COUNT(*) AS total_companies
FROM sectors
GROUP BY broad_sector
ORDER BY total_companies DESC;


-- Q7. Companies with highest Debt-to-Equity Ratio
SELECT
    company_id,
    year,
    debt_to_equity
FROM financial_ratios
ORDER BY debt_to_equity DESC
LIMIT 10;


-- Q8. Average Closing Price for each Company
SELECT
    company_id,
    AVG(close_price) AS average_close_price
FROM stock_prices
GROUP BY company_id
ORDER BY average_close_price DESC
LIMIT 10;


-- Q9. Companies having more than 10 years of Profit & Loss data
SELECT
    company_id,
    COUNT(year) AS total_years
FROM profitandloss
WHERE year IS NOT NULL
GROUP BY company_id
HAVING COUNT(year) > 10
ORDER BY total_years DESC;


-- Q10. Join Companies with Sectors
SELECT
    c.company_name,
    s.broad_sector,
    s.sub_sector
FROM companies c
JOIN sectors s
ON c.id = s.company_id
ORDER BY c.company_name;


