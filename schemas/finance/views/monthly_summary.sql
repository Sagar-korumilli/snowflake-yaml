CREATE OR REPLACE VIEW finance.monthly_summary AS
SELECT TO_CHAR(transaction_date, 'YYYY-MM') AS month, SUM(amount) AS total
FROM finance.transactions
GROUP BY month;
