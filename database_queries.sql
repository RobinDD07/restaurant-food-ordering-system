-- ============================================================================
-- RESTAURANT FOOD ORDERING SYSTEM — DATABASE SCHEMA & DBMS DEMONSTRATION QUERIES
-- DBMS Course Project
-- Database Engine: MySQL 8.0
-- ============================================================================

-- ----------------------------------------------------------------------------
-- SECTION 1: DATABASE INITIALIZATION
-- ----------------------------------------------------------------------------
CREATE DATABASE IF NOT EXISTS restaurant_food_ordering;
USE restaurant_food_ordering;

-- ----------------------------------------------------------------------------
-- SECTION 2: TABLE CREATION (DDL) — 7 REQUIRED TABLES + ORDER_ITEMS EXTENSION
-- ----------------------------------------------------------------------------

-- 1. SUPPLIER Table
-- PK: supplier_id
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS feedback;
DROP TABLE IF EXISTS order_details;
DROP TABLE IF EXISTS food;
DROP TABLE IF EXISTS agents;
DROP TABLE IF EXISTS restaurant;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS supplier;

CREATE TABLE supplier (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_name VARCHAR(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. RESTAURANT Table
-- PK: restaurant_id
-- FK: supplier_id REFERENCES supplier(supplier_id)
CREATE TABLE restaurant (
    restaurant_id INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_name VARCHAR(150) NOT NULL,
    restaurant_ph_no VARCHAR(20) NOT NULL,
    restaurant_adrs VARCHAR(255) NOT NULL,
    rating DECIMAL(3, 1) NOT NULL CHECK (rating >= 0.0 AND rating <= 5.0),
    supplier_id INT NOT NULL,
    CONSTRAINT fk_restaurant_supplier FOREIGN KEY (supplier_id) 
        REFERENCES supplier(supplier_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. FOOD Table
-- PK: food_id
-- FK: restaurant_id REFERENCES restaurant(restaurant_id)
CREATE TABLE food (
    food_id INT AUTO_INCREMENT PRIMARY KEY,
    food_name VARCHAR(150) NOT NULL,
    food_price DECIMAL(10, 2) NOT NULL CHECK (food_price > 0),
    food_rating DECIMAL(3, 1) NOT NULL CHECK (food_rating >= 0.0 AND food_rating <= 5.0),
    restaurant_id INT NOT NULL,
    CONSTRAINT fk_food_restaurant FOREIGN KEY (restaurant_id) 
        REFERENCES restaurant(restaurant_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. AGENTS Table
-- PK: agent_id
-- FK: supplier_id REFERENCES supplier(supplier_id)
CREATE TABLE agents (
    agent_id INT AUTO_INCREMENT PRIMARY KEY,
    agent_name VARCHAR(120) NOT NULL,
    agent_ph_number VARCHAR(20) NOT NULL,
    supplier_id INT NOT NULL,
    CONSTRAINT fk_agents_supplier FOREIGN KEY (supplier_id) 
        REFERENCES supplier(supplier_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. CUSTOMER Table
-- PK: cust_id
CREATE TABLE customer (
    cust_id INT AUTO_INCREMENT PRIMARY KEY,
    cust_name VARCHAR(120) NOT NULL,
    cust_adrs VARCHAR(255) NOT NULL,
    cust_ph_no VARCHAR(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. ORDER_DETAILS Table
-- PK: order_id
-- FK: cust_id REFERENCES customer(cust_id)
-- FK: supplier_id REFERENCES supplier(supplier_id)
CREATE TABLE order_details (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    cust_id INT NOT NULL,
    supplier_id INT NOT NULL,
    order_date DATE NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    CONSTRAINT fk_order_customer FOREIGN KEY (cust_id) 
        REFERENCES customer(cust_id) ON DELETE CASCADE,
    CONSTRAINT fk_order_supplier FOREIGN KEY (supplier_id) 
        REFERENCES supplier(supplier_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. FEEDBACK Table
-- PK: feedback_id
-- FK: cust_id REFERENCES customer(cust_id)
CREATE TABLE feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    cust_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    message TEXT NOT NULL,
    feedback_date DATE NOT NULL,
    CONSTRAINT fk_feedback_customer FOREIGN KEY (cust_id) 
        REFERENCES customer(cust_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 8. ORDER_ITEMS Table (Supplementary table)
-- Enables orders to itemize specific food dishes
-- PK: order_item_id
-- FK: order_id REFERENCES order_details(order_id)
-- FK: food_id REFERENCES food(food_id)
CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    food_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1 CHECK (quantity > 0),
    item_price DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_orderitems_order FOREIGN KEY (order_id) 
        REFERENCES order_details(order_id) ON DELETE CASCADE,
    CONSTRAINT fk_orderitems_food FOREIGN KEY (food_id) 
        REFERENCES food(food_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ----------------------------------------------------------------------------
-- SECTION 3: SAMPLE DATA INSERTION (DML)
-- ----------------------------------------------------------------------------

-- Insert Suppliers
INSERT INTO supplier (supplier_id, supplier_name) VALUES
(1, 'FreshFarm Agro Logistics'),
(2, 'Metro Ocean & Meat Supplies'),
(3, 'Royal Dairy & Baking Goods'),
(4, 'Golden Grain & Spice Co.');

-- Insert Restaurants
INSERT INTO restaurant (restaurant_id, restaurant_name, restaurant_ph_no, restaurant_adrs, rating, supplier_id) VALUES
(1, 'Spice Symphony Bistro', '9820123456', '14 Brigade Road, Bangalore', 4.8, 1),
(2, 'Dragon Wok Asian Kitchen', '9833456789', '22 Indiranagar 100ft Rd, Bangalore', 4.5, 2),
(3, 'Bella Italia Trattoria', '9844567890', '7 Koramangala 4th Block, Bangalore', 4.7, 3),
(4, 'Biryani Darbar Palace', '9855678901', '55 Commercial Street, Bangalore', 4.9, 4);

-- Insert Food Items
INSERT INTO food (food_id, food_name, food_price, food_rating, restaurant_id) VALUES
(1, 'Paneer Tikka Masala', 320.00, 4.8, 1),
(2, 'Dal Makhani Deluxe', 240.00, 4.6, 1),
(3, 'Butter Garlic Naan', 60.00, 4.7, 1),
(4, 'Kung Pao Chicken', 380.00, 4.5, 2),
(5, 'Hakka Noodles Special', 220.00, 4.3, 2),
(6, 'Steamed Dim Sums (6 pcs)', 260.00, 4.7, 2),
(7, 'Woodfire Margherita Pizza', 450.00, 4.9, 3),
(8, 'Creamy Fettuccine Alfredo', 390.00, 4.6, 3),
(9, 'Classic Tiramisu', 250.00, 4.8, 3),
(10, 'Hyderabadi Dum Biryani', 350.00, 4.9, 4),
(11, 'Mutton Galouti Kebab', 420.00, 4.8, 4),
(12, 'Shahi Gulab Jamun (2 pcs)', 120.00, 4.5, 4);

-- Insert Agents
INSERT INTO agents (agent_id, agent_name, agent_ph_number, supplier_id) VALUES
(1, 'Rahul Verma', '9112233445', 1),
(2, 'Sneha Kulkarni', '9223344556', 2),
(3, 'Mohammed Ali', '9334455667', 3),
(4, 'Pooja Sharma', '9445566778', 4);

-- Insert Customers
INSERT INTO customer (cust_id, cust_name, cust_adrs, cust_ph_no) VALUES
(1, 'Amit Patel', 'Flat 302, Palm Meadows, Whitefield', '9898012345'),
(2, 'Priya Nair', 'House 12, Rainbow Layout, HSR Layout', '9898123456'),
(3, 'Rohan Gupta', 'Tower B-401, Prestige Oasis, Electronic City', '9898234567'),
(4, 'Ananya Roy', 'Villa 5, Lakeview Estate, Bellandur', '9898345678');

-- Insert Order Details
INSERT INTO order_details (order_id, cust_id, supplier_id, order_date, quantity, price) VALUES
(1, 1, 1, CURDATE() - INTERVAL 2 DAY, 3, 620.00),
(2, 2, 3, CURDATE() - INTERVAL 1 DAY, 2, 840.00),
(3, 3, 4, CURDATE(), 3, 820.00),
(4, 4, 2, CURDATE(), 2, 640.00);

-- Insert Feedback
INSERT INTO feedback (feedback_id, cust_id, rating, message, feedback_date) VALUES
(1, 1, 5, 'Outstanding paneer tikka and hot crispy naan! Arrived super fast and fresh.', CURDATE() - INTERVAL 2 DAY),
(2, 2, 5, 'The woodfire pizza from Bella Italia was authentic and delicious! Great packaging.', CURDATE() - INTERVAL 1 DAY),
(3, 3, 4, 'Dum Biryani flavor was aromatic and well cooked. Delivery was prompt.', CURDATE()),
(4, 4, 4, 'Good Asian dishes and tasty sauces. Will definitely reorder again.', CURDATE());

-- Insert Order Items
INSERT INTO order_items (order_item_id, order_id, food_id, quantity, item_price) VALUES
(1, 1, 1, 1, 320.00),
(2, 1, 2, 1, 240.00),
(3, 1, 3, 1, 60.00),
(4, 2, 7, 1, 450.00),
(5, 2, 8, 1, 390.00),
(6, 3, 10, 2, 350.00),
(7, 3, 12, 1, 120.00),
(8, 4, 4, 1, 380.00),
(9, 4, 6, 1, 260.00);


-- ----------------------------------------------------------------------------
-- SECTION 4: DEMONSTRATION QUERIES FOR EVALUATION (VIVA & LAB EXAM)
-- ----------------------------------------------------------------------------

-- Q1. Basic SELECT and Filtering with WHERE
-- Find all food items priced under 300 with rating 4.5 or higher
SELECT food_id, food_name, food_price, food_rating
FROM food
WHERE food_price < 300.00 AND food_rating >= 4.5
ORDER BY food_price ASC;

-- Q2. Pattern Matching with LIKE
-- Find all customers residing in 'Layout' or 'Meadows'
SELECT cust_id, cust_name, cust_adrs, cust_ph_no
FROM customer
WHERE cust_adrs LIKE '%Layout%' OR cust_adrs LIKE '%Meadows%';

-- Q3. Range Filtering with BETWEEN
-- Find restaurants with rating between 4.6 and 5.0
SELECT restaurant_id, restaurant_name, rating, restaurant_ph_no
FROM restaurant
WHERE rating BETWEEN 4.6 AND 5.0
ORDER BY rating DESC;

-- Q4. INNER JOIN between Two Tables
-- Display all food items along with the restaurant they belong to
SELECT f.food_name, f.food_price, f.food_rating, r.restaurant_name, r.restaurant_adrs
FROM food f
INNER JOIN restaurant r ON f.restaurant_id = r.restaurant_id;

-- Q5. Multi-Table INNER JOIN (3 Tables)
-- Display Order details with Customer Name and Fulfilling Supplier Name
SELECT o.order_id, c.cust_name, c.cust_ph_no, s.supplier_name, o.order_date, o.quantity, o.price
FROM order_details o
INNER JOIN customer c ON o.cust_id = c.cust_id
INNER JOIN supplier s ON o.supplier_id = s.supplier_id
ORDER BY o.order_id ASC;

-- Q6. Multi-Table JOIN with ORDER_ITEMS (4 Tables)
-- Itemized order breakdown showing order ID, customer name, food name, unit price, quantity, and subtotal
SELECT 
    o.order_id,
    c.cust_name,
    f.food_name,
    oi.quantity,
    oi.item_price,
    (oi.quantity * oi.item_price) AS subtotal
FROM order_items oi
INNER JOIN order_details o ON oi.order_id = o.order_id
INNER JOIN customer c ON o.cust_id = c.cust_id
INNER JOIN food f ON oi.food_id = f.food_id
ORDER BY o.order_id, oi.order_item_id;

-- Q7. Aggregate Functions: COUNT, SUM, AVG, MIN, MAX
-- Total orders, total revenue, average order value, minimum and maximum order price
SELECT 
    COUNT(order_id) AS total_orders,
    SUM(price) AS total_sales_revenue,
    AVG(price) AS average_order_value,
    MIN(price) AS minimum_order_value,
    MAX(price) AS maximum_order_value,
    SUM(quantity) AS total_items_sold
FROM order_details;

-- Q8. GROUP BY with COUNT and AVG
-- Restaurant-wise menu analysis: total items offered and average item price
SELECT 
    r.restaurant_id,
    r.restaurant_name,
    COUNT(f.food_id) AS total_menu_items,
    ROUND(AVG(f.food_price), 2) AS avg_menu_price,
    MAX(f.food_price) AS max_price_dish
FROM restaurant r
LEFT JOIN food f ON r.restaurant_id = f.restaurant_id
GROUP BY r.restaurant_id, r.restaurant_name;

-- Q9. GROUP BY with HAVING Clause
-- Find suppliers associated with more than 0 delivery agents
SELECT 
    s.supplier_id,
    s.supplier_name,
    COUNT(a.agent_id) AS total_agents
FROM supplier s
INNER JOIN agents a ON s.supplier_id = a.supplier_id
GROUP BY s.supplier_id, s.supplier_name
HAVING total_agents >= 1;

-- Q10. Subquery (Nested Query)
-- Find all customers who have placed an order with price greater than average order price
SELECT cust_id, cust_name, cust_ph_no
FROM customer
WHERE cust_id IN (
    SELECT cust_id 
    FROM order_details 
    WHERE price > (SELECT AVG(price) FROM order_details)
);

-- Q11. UPDATE Query demonstration
-- Update phone number for customer #1
UPDATE customer 
SET cust_ph_no = '9898099999' 
WHERE cust_id = 1;

-- Q12. DELETE Query demonstration
-- (Run inside transaction to demonstrate without permanent data loss)
START TRANSACTION;
DELETE FROM feedback WHERE rating <= 2;
ROLLBACK;
