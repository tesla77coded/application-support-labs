INSERT INTO users (id, name, email, status) VALUES
(101, 'Rahul', 'rahul@example.com', 'active'),
(102, 'Priya', 'priya@example.com', 'active'),
(103, 'Amit', 'amit@example.com', 'inactive'),
(104, 'Sarah', 'sarah@example.com', 'active');

INSERT INTO orders (id, user_id, amount, status) VALUES
(5001, 101, 2500, 'completed'),
(5002, 102, 1800, 'pending'),
(5003, 101, 3200, 'completed'),
(5004, 103, 950, 'cancelled'),
(5005, 104, 4100, 'pending');

INSERT INTO payments (id, order_id, amount, status) VALUES
(9001, 5001, 2500, 'success'),
(9002, 5002, 1800, 'success'),
(9003, 5003, 3200, 'success'),
(9004, 5004, 950, 'failed'),
(9005, 5005, 4100, 'pending');
