CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255),
    status VARCHAR(20)
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    amount DECIMAL(10, 2),
    status VARCHAR(20),
    FOREIGN KEY (user_id) PREFERENCES users(id)
);

CREATE TABLE payments (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    amount DECIMAL(10,2),
    status VARCHAR(20),
    FOREIGN KEY (order_id) PREFERENCES orders(id)
);
