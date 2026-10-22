CREATE TABLE customers(
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_unique_id VARCHAR(50),
    customer_city VARCHAR(50),
    customer_state VARCHAR(2)
);

CREATE TABLE orders(
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) UNIQUE NOT NULL,
    order_status VARCHAR(50),
    order_purchase_timestamp DATE,
    total_units_in_order INT,
    total_order_price NUMERIC,
    order_category VARCHAR(50),

    FOREIGN KEY (customer_id) 
        REFERENCES customers(customer_id)
);

CREATE TABLE products(
    product_id VARCHAR(50) PRIMARY KEY,
    product_category VARCHAR(50)
);

CREATE TABLE sellers(
    seller_id VARCHAR(50) PRIMARY KEY,
    seller_city VARCHAR(50),
    seller_state VARCHAR(2)
);

CREATE TABLE order_items(
    order_id VARCHAR(50),
    order_item_id INT,
    product_id VARCHAR(50) NOT NULL,
    seller_id VARCHAR(50) NOT NULL,
    price NUMERIC,
    freight_value NUMERIC,

    PRIMARY KEY (order_id, order_item_id),
    FOREIGN KEY (order_id)
        REFERENCES orders(order_id),
    FOREIGN KEY (product_id)
        REFERENCES products(product_id),
    FOREIGN KEY (seller_id)
        REFERENCES sellers(seller_id)
);

CREATE TABLE order_payments(
    order_id VARCHAR(50),
    payment_sequential INT,
    payment_type VARCHAR(50),
    payment_installments INT,
    payment_value NUMERIC,

    PRIMARY KEY (order_id, payment_sequential),
    FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
);

CREATE TABLE order_reviews(
    review_id VARCHAR(50),
    order_id VARCHAR(50),
    review_score INT,

    PRIMARY KEY (review_id, order_id),
    FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
);