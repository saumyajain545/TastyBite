CREATE DATABASE IF NOT EXISTS tastybite
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE tastybite;

CREATE TABLE IF NOT EXISTS menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    description VARCHAR(255) NOT NULL DEFAULT '',
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    rating DECIMAL(2,1) NOT NULL DEFAULT 4.5,
    image_url VARCHAR(500) NOT NULL,
    is_available BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(120) NOT NULL,
    email VARCHAR(190) NOT NULL,
    phone VARCHAR(30) NOT NULL,
    address TEXT NOT NULL,
    notes TEXT,
    total DECIMAL(10,2) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'Received',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    menu_item_id INT NULL,
    item_name VARCHAR(120) NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS contact_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(190) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO menu_items (name, description, category, price, rating, image_url)
SELECT 'Margherita Pizza', 'Classic cheese pizza with tomato and basil', 'Pizza', 199.00, 4.5,
'https://images.unsplash.com/photo-1579751626657-72bc17010498?auto=format&fit=crop&w=900&q=80'
WHERE NOT EXISTS (SELECT 1 FROM menu_items WHERE name='Margherita Pizza');
INSERT INTO menu_items (name, description, category, price, rating, image_url)
SELECT 'White Sauce Pasta', 'Creamy pasta with herbs and parmesan', 'Pasta', 169.00, 4.3,
'https://images.unsplash.com/photo-1473093295043-cdd812d0e601?auto=format&fit=crop&w=900&q=80'
WHERE NOT EXISTS (SELECT 1 FROM menu_items WHERE name='White Sauce Pasta');
INSERT INTO menu_items (name, description, category, price, rating, image_url)
SELECT 'Paneer Tikka', 'Smoky paneer with peppers and Indian spices', 'Indian', 189.00, 4.4,
'https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?auto=format&fit=crop&w=900&q=80'
WHERE NOT EXISTS (SELECT 1 FROM menu_items WHERE name='Paneer Tikka');
INSERT INTO menu_items (name, description, category, price, rating, image_url)
SELECT 'Veg Burger', 'Crispy patty, fresh lettuce and house sauce', 'Burgers', 149.00, 4.2,
'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=900&q=80'
WHERE NOT EXISTS (SELECT 1 FROM menu_items WHERE name='Veg Burger');
INSERT INTO menu_items (name, description, category, price, rating, image_url)
SELECT 'French Fries', 'Golden crispy fries with seasoning', 'Sides', 99.00, 4.1,
'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&w=900&q=80'
WHERE NOT EXISTS (SELECT 1 FROM menu_items WHERE name='French Fries');
INSERT INTO menu_items (name, description, category, price, rating, image_url)
SELECT 'Garlic Bread', 'Toasted bread with garlic butter', 'Sides', 129.00, 4.3,
'https://images.unsplash.com/photo-1619531040576-f9416740661b?auto=format&fit=crop&w=900&q=80'
WHERE NOT EXISTS (SELECT 1 FROM menu_items WHERE name='Garlic Bread');
INSERT INTO menu_items (name, description, category, price, rating, image_url)
SELECT 'Choco Lava Cake', 'Warm chocolate cake with a molten centre', 'Desserts', 149.00, 4.6,
'https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=900&q=80'
WHERE NOT EXISTS (SELECT 1 FROM menu_items WHERE name='Choco Lava Cake');
INSERT INTO menu_items (name, description, category, price, rating, image_url)
SELECT 'Cold Coffee', 'Chilled coffee with creamy foam', 'Beverages', 119.00, 4.4,
'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=900&q=80'
WHERE NOT EXISTS (SELECT 1 FROM menu_items WHERE name='Cold Coffee');
