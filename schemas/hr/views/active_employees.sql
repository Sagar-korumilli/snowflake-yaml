CREATE OR REPLACE VIEW hr.active_employees AS
SELECT * FROM hr.employees
WHERE CURRENT_DATE - hire_date < 365;
