import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# Глобальные переменные для хранения состояния
current_receipt = []
conn = None
tree = None
receipt_tree = None
sales_tree = None
total_label = None
product_combo = None
name_entry = None
price_entry = None
quantity_entry = None
sale_quantity = None

def create_tables():
    """Создание таблиц в базе данных"""
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sale_date TEXT,
        total_amount REAL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sale_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sale_id INTEGER,
        product_id INTEGER,
        product_name TEXT,
        quantity INTEGER,
        price REAL,
        total REAL,
        FOREIGN KEY (sale_id) REFERENCES sales(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
    ''')
    
    conn.commit()

def load_products():
    """Загрузка списка товаров"""
    for item in tree.get_children():
        tree.delete(item)
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    
    for product in products:
        tree.insert('', 'end', values=product)
    
    cursor.execute("SELECT id, name FROM products WHERE quantity > 0")
    product_combo['values'] = [f"{p[0]}: {p[1]}" for p in cursor.fetchall()]
    if product_combo['values']:
        product_combo.current(0)

def load_sales():
    """Загрузка истории продаж"""
    for item in sales_tree.get_children():
        sales_tree.delete(item)
    
    cursor = conn.cursor()
    cursor.execute("SELECT id, sale_date, total_amount FROM sales ORDER BY sale_date DESC")
    sales = cursor.fetchall()
    
    for sale in sales:
        sales_tree.insert('', 'end', values=sale)

def select_product(event):
    """Заполнение полей при выборе товара"""
    selected = tree.focus()
    if selected:
        values = tree.item(selected, 'values')
        name_entry.delete(0, 'end')
        name_entry.insert(0, values[1])
        price_entry.delete(0, 'end')
        price_entry.insert(0, values[2])
        quantity_entry.delete(0, 'end')
        quantity_entry.insert(0, values[3])

def add_product():
    """Добавление нового товара"""
    try:
        name = name_entry.get()
        price = float(price_entry.get())
        quantity = int(quantity_entry.get())
        
        if not name:
            messagebox.showerror("Ошибка", "Введите название")
            return
        
        if price <= 0 or quantity < 0:
            messagebox.showerror("Ошибка", "Цена и количество должны быть положительными")
            return
        
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO products (name, price, quantity)
        VALUES (?, ?, ?)
        ''', (name, price, quantity))
        conn.commit()
        
        load_products()
        
        name_entry.delete(0, 'end')
        price_entry.delete(0, 'end')
        quantity_entry.delete(0, 'end')
        
        messagebox.showinfo("Успех", "Товар добавлен")
    except ValueError:
        messagebox.showerror("Ошибка", "Некорректные данные")

def delete_product():
    """Удаление товара"""
    selected = tree.focus()
    if not selected:
        messagebox.showerror("Ошибка", "Выберите товар")
        return
    
    if not messagebox.askyesno("Подтверждение", "Удалить товар?"):
        return
    
    product_id = tree.item(selected, 'values')[0]
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    
    load_products()
    messagebox.showinfo("Успех", "Товар удален")

def add_to_receipt():
    """Добавление товара в чек"""
    global current_receipt
    
    product_str = product_combo.get()
    if not product_str:
        messagebox.showerror("Ошибка", "Выберите товар")
        return
    
    try:
        quantity = int(sale_quantity.get())
        if quantity <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректное количество")
        return
    
    product_id = int(product_str.split(':')[0])
    product_name = product_str.split(':')[1].strip()
    
    cursor = conn.cursor()
    cursor.execute("SELECT price, quantity FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    
    if not product:
        messagebox.showerror("Ошибка", "Товар не найден")
        return
    
    price, available = product
    
    if quantity > available:
        messagebox.showerror("Ошибка", f"Недостаточно товара (доступно: {available})")
        return
    
    current_receipt.append({
        'product_id': product_id,
        'product_name': product_name,
        'quantity': quantity,
        'price': price,
        'total': price * quantity
    })
    
    update_receipt_tree()

def update_receipt_tree():
    """Обновление отображения чека"""
    global current_receipt
    
    for item in receipt_tree.get_children():
        receipt_tree.delete(item)
    
    total_amount = 0
    for item in current_receipt:
        receipt_tree.insert('', 'end', values=(
            item['product_name'],
            item['quantity'],
            item['price'],
            item['total']
        ))
        total_amount += item['total']
    
    total_label.config(text=f"{total_amount:.2f}")

def clear_receipt():
    """Очистка текущего чека"""
    global current_receipt
    current_receipt = []
    update_receipt_tree()
    total_label.config(text="0.00")

def finalize_sale():
    """Оформление продажи"""
    global current_receipt
    
    if not current_receipt:
        messagebox.showerror("Ошибка", "Чек пуст")
        return
    
    try:
        cursor = conn.cursor()
        
        total_amount = sum(item['total'] for item in current_receipt)
        sale_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
        INSERT INTO sales (sale_date, total_amount)
        VALUES (?, ?)
        ''', (sale_date, total_amount))
        
        sale_id = cursor.lastrowid
        
        for item in current_receipt:
            cursor.execute('''
            INSERT INTO sale_items (sale_id, product_id, product_name, quantity, price, total)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                sale_id,
                item['product_id'],
                item['product_name'],
                item['quantity'],
                item['price'],
                item['total']
            ))
            
            cursor.execute('''
            UPDATE products 
            SET quantity = quantity - ?
            WHERE id = ?
            ''', (item['quantity'], item['product_id']))
        
        conn.commit()
        
        clear_receipt()
        load_products()
        load_sales()
        
        messagebox.showinfo("Успех", "Продажа оформлена")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
        conn.rollback()

def show_sale_details(event):
    """Показ деталей выбранной продажи"""
    selected = sales_tree.focus()
    if not selected:
        return
    
    sale_id = sales_tree.item(selected, 'values')[0]
    
    for item in receipt_tree.get_children():
        receipt_tree.delete(item)
    
    cursor = conn.cursor()
    cursor.execute('''
    SELECT product_name, quantity, price, total 
    FROM sale_items 
    WHERE sale_id = ?
    ''', (sale_id,))
    
    for row in cursor.fetchall():
        receipt_tree.insert('', 'end', values=row)
    
    total = sum(float(receipt_tree.item(item, 'values')[3]) 
              for item in receipt_tree.get_children())
    total_label.config(text=f"{total:.2f}")

def setup_ui(root):
    """Настройка пользовательского интерфейса"""
    global tree, receipt_tree, sales_tree, total_label, product_combo
    global name_entry, price_entry, quantity_entry, sale_quantity
    
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)
    
    # Вкладка товаров
    products_tab = ttk.Frame(notebook)
    notebook.add(products_tab, text="Товары")
    
    frame = ttk.Frame(products_tab)
    frame.pack(pady=10)
    
    ttk.Label(frame, text="Название:").grid(row=0, column=0, padx=5, pady=5)
    name_entry = ttk.Entry(frame, width=30)
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    
    ttk.Label(frame, text="Цена:").grid(row=1, column=0, padx=5, pady=5)
    price_entry = ttk.Entry(frame, width=30)
    price_entry.grid(row=1, column=1, padx=5, pady=5)
    
    ttk.Label(frame, text="Количество:").grid(row=2, column=0, padx=5, pady=5)
    quantity_entry = ttk.Entry(frame, width=30)
    quantity_entry.grid(row=2, column=1, padx=5, pady=5)
    
    ttk.Button(frame, text="Добавить", command=add_product).grid(row=3, column=0, pady=10)
    ttk.Button(frame, text="Удалить", command=delete_product).grid(row=3, column=1, pady=10)
    
    tree = ttk.Treeview(products_tab, columns=('id', 'name', 'price', 'quantity'), show='headings')
    tree.heading('id', text='ID')
    tree.heading('name', text='Название')
    tree.heading('price', text='Цена')
    tree.heading('quantity', text='Количество')
    tree.pack(fill='both', expand=True)
    
    tree.bind('<<TreeviewSelect>>', select_product)
    
    # Вкладка продаж
    sales_tab = ttk.Frame(notebook)
    notebook.add(sales_tab, text="Продажи")
    
    frame = ttk.LabelFrame(sales_tab, text="Формирование чека")
    frame.pack(pady=10, padx=10, fill='x')
    
    ttk.Label(frame, text="Товар:").grid(row=0, column=0, padx=5, pady=5)
    product_combo = ttk.Combobox(frame, state="readonly", width=30)
    product_combo.grid(row=0, column=1, padx=5, pady=5)
    
    ttk.Label(frame, text="Количество:").grid(row=1, column=0, padx=5, pady=5)
    sale_quantity = ttk.Spinbox(frame, from_=1, to=1000, width=10)
    sale_quantity.grid(row=1, column=1, padx=5, pady=5, sticky='w')
    
    ttk.Button(frame, text="Добавить в чек", command=add_to_receipt).grid(
        row=2, column=0, columnspan=2, pady=10)
    
    receipt_frame = ttk.LabelFrame(sales_tab, text="Текущий чек")
    receipt_frame.pack(pady=10, padx=10, fill='both', expand=True)
    
    receipt_tree = ttk.Treeview(receipt_frame, columns=('product', 'quantity', 'price', 'total'), show='headings')
    receipt_tree.heading('product', text='Товар')
    receipt_tree.heading('quantity', text='Количество')
    receipt_tree.heading('price', text='Цена')
    receipt_tree.heading('total', text='Сумма')
    receipt_tree.pack(fill='both', expand=True)
    
    ttk.Label(receipt_frame, text="Итого:").pack(side='left', padx=5, pady=5)
    total_label = ttk.Label(receipt_frame, text="0.00")
    total_label.pack(side='left', padx=5, pady=5)
    
    btn_frame = ttk.Frame(sales_tab)
    btn_frame.pack(pady=10)
    
    ttk.Button(btn_frame, text="Оформить продажу", command=finalize_sale).pack(side='left', padx=5)
    ttk.Button(btn_frame, text="Очистить чек", command=clear_receipt).pack(side='left', padx=5)
    
    history_frame = ttk.LabelFrame(sales_tab, text="История продаж")
    history_frame.pack(pady=10, padx=10, fill='both', expand=True)
    
    sales_tree = ttk.Treeview(history_frame, columns=('id', 'date', 'total'), show='headings')
    sales_tree.heading('id', text='ID')
    sales_tree.heading('date', text='Дата')
    sales_tree.heading('total', text='Сумма')
    sales_tree.pack(fill='both', expand=True)
    
    sales_tree.bind('<<TreeviewSelect>>', show_sale_details)


    
def main():
    
    global conn
    
    root = tk.Tk()
    root.title("Система учета товаров с чеком")
    root.geometry("900x700")
    
    # Подключение к базе данных
    conn = sqlite3.connect('store_with_receipt.db')
    create_tables()
    
    # Настройка интерфейса
    setup_ui(root)
    
    # Загрузка данных
    load_products()
    load_sales()
    
    root.mainloop()
    
    # Закрытие соединения при выходе
    if conn:
        conn.close()

if __name__ == "__main__":
    main()
