CREATE OR REPLACE VIEW operations.logistics_summary AS
SELECT location, COUNT(*) AS item_count, SUM(quantity) AS total_quantity
FROM operations.supply_chain
GROUP BY location;
