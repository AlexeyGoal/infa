
import sqlite3

def create_database():
    conn = sqlite3.connect('sport_store.db')
    cursor = conn.cursor()
    
    # Таблица категорий
    cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
                    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    description TEXT)''')
    
    # Таблица брендов
    cursor.execute('''CREATE TABLE IF NOT EXISTS brands (
                    brand_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    country TEXT,
                    founded_year INTEGER)''')
    
    # Таблица поставщиков
    cursor.execute('''CREATE TABLE IF NOT EXISTS suppliers (
                    supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    contact_person TEXT,
                    phone TEXT,
                    email TEXT)''')
    
    # Таблица товаров
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    category_id INTEGER,
                    brand_id INTEGER,
                    supplier_id INTEGER,
                    price REAL NOT NULL,
                    quantity INTEGER,
                    description TEXT,
                    FOREIGN KEY (category_id) REFERENCES categories(category_id),
                    FOREIGN KEY (brand_id) REFERENCES brands(brand_id),
                    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id))''')
    
    # Таблица клиентов
    cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    phone TEXT UNIQUE,
                    email TEXT,
                    registration_date TEXT)''')
    
    # Таблица заказов
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER,
                    order_date TEXT NOT NULL UNIQUE,
                    total_amount REAL,
                    status TEXT,
                    FOREIGN KEY (customer_id) REFERENCES customers(customer_id))''')
    
    # Таблица позиций заказа
    cursor.execute('''CREATE TABLE IF NOT EXISTS order_items (
                    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER,
                    product_id INTEGER,
                    quantity INTEGER,
                    price REAL,
                    UNIQUE(order_id, product_id),
                    FOREIGN KEY (order_id) REFERENCES orders(order_id),
                    FOREIGN KEY (product_id) REFERENCES products(product_id))''')
    

    fill_test_data(cursor)
    conn.commit()
    conn.close()

def fill_test_data(cursor):
    # Категории
    with open('categories.txt', 'r', encoding='utf-8') as file:
        categories = [line.strip().split(' | ') for line in file if line.strip()]
    cursor.executemany("INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)", categories)
    
    # Бренды
    with open('brands.txt', 'r', encoding='utf-8') as file:
        brands = [line.strip().split(' | ') for line in file if line.strip()]
        brands = [(name, country, int(year)) for name, country, year in brands]
    cursor.executemany("INSERT OR IGNORE INTO brands (name, country, founded_year) VALUES (?, ?, ?)", brands)
    
    # Поставщики
    with open('suppliers.txt', 'r', encoding='utf-8') as file:
        suppliers = [line.strip().split(' | ') for line in file if line.strip()]
    cursor.executemany("""
    INSERT OR IGNORE INTO suppliers (name, contact_person, phone, email) 
    VALUES (?, ?, ?, ?)
    """, suppliers)
    
    # Товары
    with open('items.txt', 'r', encoding='utf-8') as file:
        products = [line.strip().split(' | ') for line in file if line.strip()]
        products = [(name, int(cat_id), int(brand_id), int(supp_id), 
                    float(price), int(quant), desc) 
                    for name, cat_id, brand_id, supp_id, price, quant, desc in products]
    cursor.executemany("""
    INSERT OR IGNORE INTO products (name, category_id, brand_id, supplier_id, 
                        price, quantity, description)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, products)
    
    # Клиенты
    with open('clients.txt', 'r', encoding='utf-8') as file:
        customers = [line.strip().split(' | ') for line in file if line.strip()]
    cursor.executemany("""
    INSERT OR IGNORE INTO customers (first_name, last_name, phone, email, registration_date)
    VALUES (?, ?, ?, ?, ?)
    """, customers)
    

    
    # Заказы
    with open('orders.txt', 'r', encoding='utf-8') as file:
        orders = [line.strip().split(' | ') for line in file if line.strip()]
        orders = [(int(cust_id), date, float(amount), status) for cust_id, date, amount, status in orders]
    cursor.executemany("""
    INSERT OR IGNORE INTO orders (customer_id, order_date, total_amount, status)
    VALUES (?, ?, ?, ?)
    """, orders)
    
    # Позиции заказов
    with open('order_items.txt', 'r', encoding='utf-8') as file:
        order_items = [line.strip().split(' | ') for line in file if line.strip()]
        order_items = [(int(order_id), int(product_id), int(quantity), float(price))
                  for order_id, product_id, quantity, price in order_items]
    cursor.executemany('''INSERT OR IGNORE INTO order_items (order_id, product_id, quantity, price) 
                       VALUES (?, ?, ?, ?)''', order_items)

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('sport_store.db')
    
    def get_products(self):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT p.product_id, p.name, c.name, b.name, p.price, p.quantity 
                       FROM products p 
                       JOIN categories c ON p.category_id = c.category_id 
                       JOIN brands b ON p.brand_id = b.brand_id''')
        return cursor.fetchall()
    
    def get_customers(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM customers")
        return cursor.fetchall()
    
    def get_orders(self):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT o.order_id, c.first_name || ' ' || c.last_name, o.order_date, o.total_amount, o.status 
                       FROM orders o 
                       JOIN customers c ON o.customer_id = c.customer_id''')
        return cursor.fetchall()
    
    def close(self):
        self.conn.close()
