-- Basics Queries
SELECT * FROM users;

SELECT id, name, status
FROM users
WHERE status = 'active';

SELECT *
FROM orders
WHERE amount > 2000;

SELECT *
FROM orders
WHERE status = 'pending';


-- Sorting and Limiting
SELECT *
FROM orders
ORDER By amount DESC
LIMIT 3;

SELECT *
FROM users
WHERE phone IS NULL;


SELECT *
FROM users
WHERE phone IS NOT NULL;


-- Aggregation
SELECT COUNT(*) FROM orders;

SELECT COUNT(*)
FROM orders
WHERE status = 'pending';

SELECT SUM(amount)
FROM orders
WHERE status = 'completed';

SELECT status, COUNT(*)
FROM orders
GROUP BY status;

SELECT status, SUM(amount)
FROM orders
GROUP BY status;


-- Joins
SELECT
    orders.id,
    orders.amount,
    orders.status,
    payments.status
FROM orders
INNER JOIN payments
    ON orders.id = payements.order_id;


-- Left Join
SELECT
    orders.id,
    orders.status,
    orders.status,
    payments.status
FROM orders
LEFT JOIN payments
    ON orders.id = payments.order_id;


-- Orders without payments
SELECT
    orders.id,
    orders.amount,
    orders.status
FROM orders
LEFT JOIN payments
    ON orders.id = payments.order_id
WHERE payments.id IS NULL;


-- Incident Investigation Query
SELECT
    orders.id AS order_id,
    orders.user_id,
    orders.amount AS order_amount,
    orders.status AS order_status,
    payments.id AS payment_id,
    payments.amount AS payment_amount
    payment.status AS payment_status
FROM orders
LEFT JOIN payments
    ON orders.id = payments.order_id
WHERE orders.id = 5005;
