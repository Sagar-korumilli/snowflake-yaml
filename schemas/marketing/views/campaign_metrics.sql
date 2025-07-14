CREATE OR REPLACE VIEW marketing.campaign_metrics AS
SELECT campaign_id, DATEDIFF(day, start_date, end_date) AS duration
FROM marketing.campaigns;
