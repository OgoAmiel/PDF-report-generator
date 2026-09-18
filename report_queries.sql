-- Total number of orders
SELECT COUNT(*) AS total_orders
FROM orders;

-- Total revenue
SELECT SUM(amount) AS total_revenue
FROM orders;

-- Top five products by revenue
SELECT
    product,
    SUM(amount) AS revenue
FROM orders
GROUP BY product
ORDER BY revenue DESC
LIMIT 5;

-- Orders per day over the last seven calendar days, including today
SELECT
    created_at,
    COUNT(*) AS order_count
FROM orders
WHERE created_at >= date('now', '-6 days')
GROUP BY created_at
ORDER BY created_at;