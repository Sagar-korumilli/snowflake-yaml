CREATE OR REPLACE VIEW sales.orders_summary AS
SELECT customer_id, COUNT(*) AS total_orders, SUM(amount) AS total_spent
FROM sales.orders
GROUP BY customer_id;
