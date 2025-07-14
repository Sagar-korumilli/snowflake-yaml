-- Table: transactions
CREATE OR REPLACE TABLE finance.transactions (
    transaction_id INT,
    account_id INT,
    amount NUMBER(12,2),
    transaction_date DATE
);

-- Table: accounts
CREATE OR REPLACE TABLE finance.accounts (
    account_id INT,
    customer_id INT,
    account_type STRING,
    opened_date DATE
);

-- View: recent_transactions
CREATE OR REPLACE VIEW finance.recent_transactions AS
SELECT 
    transaction_id,
    account_id,
    amount,
    transaction_date
FROM finance.transactions
WHERE transaction_date > CURRENT_DATE - INTERVAL '30 DAY';

-- Procedure: process_monthly_interest
CREATE OR REPLACE PROCEDURE finance.process_monthly_interest()
RETURNS STRING
LANGUAGE SQL
AS
$$
BEGIN
    INSERT INTO finance.transactions (transaction_id, account_id, amount, transaction_date)
    SELECT 
        seq4(),
        account_id,
        amount * 0.01,
        CURRENT_DATE
    FROM finance.accounts
    WHERE account_type = 'SAVINGS';

    RETURN 'Interest processed';
END;
$$;
