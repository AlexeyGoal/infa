import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from tkinter import *
from tkinter import font as tkfont
from ttkbootstrap import Style, Window, ttk


class SportStoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление спортивным магазином")
        self.root.geometry("1200x800")
        self.style = Style(theme="darkly")
        
        # Подключение к базе данных
        self.db = sqlite3.connect('sport_store.db')
        self.cursor = self.db.cursor()
        
        self.setup_styles()
        # Создание вкладок
        self.notebook = ttk.Notebook(root, style = "primaty.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Вкладка товаров
        self.products_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.products_tab, text="Товары")
        self.setup_products_tab()
        
        # Вкладка клиентов
        self.customers_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.customers_tab, text="Клиенты")
        self.setup_customers_tab()
        
        # Вкладка заказов
        self.orders_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.orders_tab, text="Заказы")
        self.setup_orders_tab()
        
        # Вкладка отчетов
        self.reports_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.reports_tab, text="Отчеты")
        self.setup_reports_tab()
        
        # Обновление данных при запуске
        self.update_products_list()
        self.update_customers_list()
        self.update_orders_list()
    

    
    #установка стилей
    def setup_styles(self):
        self.style.configure('Treeview', font=('Segoe UI', 9), rowheight=25)
        self.style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'))
        self.style.map('Treeview', background=[('selected', '#347083')])
        self.style.configure("Treeview.Heading", borderwidth=2)
        self.style.configure("Treeview", borderwidth=2)
        # Стиль для кнопок
        self.style.configure('TButton', font=('Segoe UI', 10), padding=5)
        
        # Стиль для полей ввода
        self.style.configure('TEntry', font=('Segoe UI', 9), padding=3)
        self.style.configure('TCombobox', font=('Segoe UI', 9), padding=3)
        self.style.configure("Treeview.Heading",
                        font=('Segoe UI', 12, 'bold'),
                        relief="solid")
                        
    
        self.style.configure("Treeview",
                        font=('Segoe UI', 11),
                        rowheight=25,
                        relief="flat")
    
        self.style.map('Treeview',
                  background=[('selected', '#347083')],
                  foreground=[('selected', 'white')])

                    # Добавляем разделители строк
        self.style.configure("Treeview.Item", 
                            padding=(0, 5)) # Отступы в строках


    def setup_products_tab(self):
        # Панель управления товарами
        control_frame = ttk.Frame(self.products_tab)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(control_frame, text="Добавить товар", command=self.add_product, bootstyle = "success").pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Редактировать", command=self.edit_product, bootstyle = "warning").pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Удалить", command=self.delete_product, bootstyle = "danger").pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Обновить", command=self.update_products_list, bootstyle = "info").pack(side=tk.LEFT, padx=2)
        
        # Поиск
        search_frame = ttk.Frame(self.products_tab)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(search_frame, text="Поиск:").pack(side=tk.LEFT)
        self.product_search_entry = ttk.Entry(search_frame)
        self.product_search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(search_frame, text="Найти", command=self.search_products, bootstyle = "info-outline").pack(side=tk.LEFT, padx=2)
        
        # Таблица товаров
        columns = ("id", "name", "category", "brand", "price", "quantity", "supplier_id")
        self.products_tree = ttk.Treeview(self.products_tab, columns=columns, show="headings", selectmode="browse")
        
        self.products_tree.heading("id", text="ID")
        self.products_tree.heading("name", text="Название")
        self.products_tree.heading("category", text="ID категории")
        self.products_tree.heading("brand", text="ID бренда")
        self.products_tree.heading("price", text="Цена")
        self.products_tree.heading("quantity", text="Количество")
        self.products_tree.heading("supplier_id", text = "ID поставщика")

        self.products_tree.column("id", width=50, anchor=tk.CENTER)
        self.products_tree.column("name", width=200)
        self.products_tree.column("category", width=130)
        self.products_tree.column("brand", width=130)
        self.products_tree.column("price", width=100, anchor=tk.E)
        self.products_tree.column("quantity", width=100, anchor=tk.CENTER)
        self.products_tree.column("supplier_id", width=90)

        scrollbar = ttk.Scrollbar(self.products_tab, orient=tk.VERTICAL, command=self.products_tree.yview)
        self.products_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.products_tree.pack(fill=tk.BOTH, expand=True)



    def setup_customers_tab(self):
        # Панель управления клиентами
        control_frame = ttk.Frame(self.customers_tab)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(control_frame, text="Добавить клиента", command=self.add_customer, bootstyle = "success").pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Редактировать", command=self.edit_customer, bootstyle = "warning").pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Удалить", command=self.delete_customer, bootstyle = "danger").pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Обновить", command=self.update_customers_list, bootstyle = "info").pack(side=tk.LEFT, padx=2)
        
        # Поиск
        search_frame = ttk.Frame(self.customers_tab)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(search_frame, text="Поиск:").pack(side=tk.LEFT)
        self.customer_search_entry = ttk.Entry(search_frame)
        self.customer_search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(search_frame, text="Найти", command=self.search_customers, bootstyle = "info-outline" ).pack(side=tk.LEFT, padx=2)
        
        # Таблица клиентов
        columns = ("id", "first_name", "last_name", "phone", "email", "reg_date")
        self.customers_tree = ttk.Treeview(self.customers_tab, columns=columns, show="headings", selectmode="browse")
        
        self.customers_tree.heading("id", text="ID")
        self.customers_tree.heading("first_name", text="Имя")
        self.customers_tree.heading("last_name", text="Фамилия")
        self.customers_tree.heading("phone", text="Телефон")
        self.customers_tree.heading("email", text="Email")
        self.customers_tree.heading("reg_date", text="Дата регистрации")
        
        self.customers_tree.column("id", width=50, anchor=tk.CENTER)
        self.customers_tree.column("first_name", width=150)
        self.customers_tree.column("last_name", width=150)
        self.customers_tree.column("phone", width=120)
        self.customers_tree.column("email", width=200)
        self.customers_tree.column("reg_date", width=120)
        
        scrollbar = ttk.Scrollbar(self.customers_tab, orient=tk.VERTICAL, command=self.customers_tree.yview, bootstyle = "round")
        self.customers_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.customers_tree.pack(fill=tk.BOTH, expand=True)

  
    
    def setup_orders_tab(self):
        # Панель управления заказами
        control_frame = ttk.Frame(self.orders_tab)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(control_frame, text="Создать заказ", command=self.create_order, bootstyle = "success").pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Просмотреть", command=self.view_order, bootstyle = "info").pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Обновить статус", command=self.update_order_status, bootstyle = "warning").pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Обновить список", command=self.update_orders_list, bootstyle = "warning").pack(side=tk.LEFT, padx=2)
        
        # Фильтры
        filter_frame = ttk.Frame(self.orders_tab)
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Статус:").pack(side=tk.LEFT)
        self.status_filter = ttk.Combobox(filter_frame, values=["Все", "Новый", "В обработке", "Выполнен", "Отменен"])
        self.status_filter.pack(side=tk.LEFT, padx=5)
        self.status_filter.set("Все")
        
        ttk.Label(filter_frame, text="Дата от:").pack(side=tk.LEFT, padx=(10, 0))
        self.date_from_entry = ttk.Entry(filter_frame, width=10)
        self.date_from_entry.pack(side=tk.LEFT)
        
        ttk.Label(filter_frame, text="до:").pack(side=tk.LEFT)
        self.date_to_entry = ttk.Entry(filter_frame, width=10)
        self.date_to_entry.pack(side=tk.LEFT)
        
        ttk.Button(filter_frame, text="Применить", command=self.filter_orders, bootstyle = "info-outline").pack(side=tk.LEFT, padx=5)
        
        # Таблица заказов
        columns = ("id", "customer", "date", "amount", "status")
        self.orders_tree = ttk.Treeview(self.orders_tab, columns=columns, show="headings", selectmode="browse")
        
        self.orders_tree.heading("id", text="ID")
        self.orders_tree.heading("customer", text="Клиент")
        self.orders_tree.heading("date", text="Дата")
        self.orders_tree.heading("amount", text="Сумма")
        self.orders_tree.heading("status", text="Статус")
        
        self.orders_tree.column("id", width=50, anchor=tk.CENTER)
        self.orders_tree.column("customer", width=200)
        self.orders_tree.column("date", width=120)
        self.orders_tree.column("amount", width=100, anchor=tk.E)
        self.orders_tree.column("status", width=120)
        
        scrollbar = ttk.Scrollbar(self.orders_tab, orient=tk.VERTICAL, command=self.orders_tree.yview, bootstyle = "round")
        self.orders_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.orders_tree.pack(fill=tk.BOTH, expand=True)
    
    def setup_reports_tab(self):
        # Панель отчетов
        report_frame = ttk.Frame(self.reports_tab)
        report_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(report_frame, text="Отчеты", font=('Helvetica', 14)).pack(pady=10)
        
        # Кнопки отчетов
        ttk.Button(report_frame, text="Товары по категориям", 
                  command=lambda: self.generate_report("category"), bootstyle = "info" ).pack(fill=tk.X, pady=5)
        ttk.Button(report_frame, text="Продажи по датам", 
                  command=lambda: self.generate_report("sales_by_date"), bootstyle = "info" ).pack(fill=tk.X, pady=5)
        ttk.Button(report_frame, text="Популярные товары", 
                  command=lambda: self.generate_report("popular_products"), bootstyle = "info" ).pack(fill=tk.X, pady=5)
        ttk.Button(report_frame, text="Клиенты по заказам", 
                  command=lambda: self.generate_report("customers_by_orders"), bootstyle = "info" ).pack(fill=tk.X, pady=5)
        
        # Область для вывода отчета
        self.report_text = tk.Text(report_frame, height=15, wrap=tk.WORD)
        self.report_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(report_frame, orient=tk.VERTICAL, command=self.report_text.yview, bootstyle = "round")
        self.report_text.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Методы для работы с товарами
    def update_products_list(self):
        self.products_tree.delete(*self.products_tree.get_children())
        products = self.db.execute('''SELECT p.product_id, p.name, c.category_id, b.brand_id, p.price, p.quantity, s.supplier_id 
                                   FROM products p 
                                   JOIN categories c ON p.category_id = c.category_id 
                                   JOIN brands b ON p.brand_id = b.brand_id
                                   JOIN suppliers s ON p.supplier_id = s.supplier_id'''
                                   ).fetchall()
        for product in products:
            self.products_tree.insert("", tk.END, values=product)
    
    def search_products(self):
        query = self.product_search_entry.get()
        if not query:
            self.update_products_list()
            return
        
        self.products_tree.delete(*self.products_tree.get_children())
        products = self.db.execute('''SELECT p.product_id, p.name, c.name, b.name, p.price, p.quantity 
                                   FROM products p 
                                   JOIN categories c ON p.category_id = c.category_id 
                                   JOIN brands b ON p.brand_id = b.brand_id
                                   WHERE p.name LIKE ? OR c.name LIKE ? OR b.name LIKE ?''', 
                                   (f"%{query}%", f"%{query}%", f"%{query}%")).fetchall()
        for product in products:
            self.products_tree.insert("", tk.END, values=product)
    
    def reset_products_search(self):
        """Сброс поиска товаров"""
        self.product_search_entry.delete(0, tk.END)
        self.update_products_list()
    
    def show_product_tooltip(self, event):
        """Показ подсказки с описанием товара"""
        item = self.products_tree.identify_row(event.y)
        if not item:
            return
        
        product_id = self.products_tree.item(item)['values'][0]
        description = self.db.execute("SELECT description FROM products WHERE product_id = ?", (product_id,)).fetchone()[0]
        
        if description:
            self.products_tree.tooltip = tk.Toplevel(self.products_tree)
            self.products_tree.tooltip.wm_overrideredirect(True)
            self.products_tree.tooltip.wm_geometry(f"+{event.x_root+15}+{event.y_root+10}")
            
            label = ttk.Label(self.products_tree.tooltip, text=description, background="#ffffe0", 
                            relief="solid", borderwidth=1, padding=5, wraplength=300)
            label.pack()
            
            self.products_tree.bind("<Leave>", lambda e: self.products_tree.tooltip.destroy())
    
    def add_product(self):
        """Добавление нового товара"""
        self.product_dialog("Добавить товар")
    
    def edit_product(self):
        """Редактирование товара"""
        selected = self.products_tree.focus()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите товар для редактирования")
            return
        
        product_id = self.products_tree.item(selected)['values'][0]
        self.product_dialog("Редактировать товар", product_id)
    
    def delete_product(self):
        """Удаление товара"""
        selected = self.products_tree.focus()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите товар для удаления")
            return
        
        product_id = self.products_tree.item(selected)['values'][0]
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этот товар?"):
            self.db.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
            self.db.commit()
            self.update_products_list()
            messagebox.showinfo("Успех", "Товар успешно удален")
    
    def product_dialog(self, title, product_id=None):
        """Диалоговое окно для добавления/редактирования товара"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("500x500")
        dialog.resizable(False, False)
        
        # Центрирование окна
        self.center_window(dialog)
        
        # Получение данных для выпадающих списков
        categories = self.db.execute("SELECT category_id, name FROM categories").fetchall()
        brands = self.db.execute("SELECT brand_id, name FROM brands").fetchall()
        suppliers = self.db.execute("SELECT supplier_id, name FROM suppliers").fetchall()
        
        # Получение данных о товаре, если редактирование
        product_data = None
        if product_id:
            product_data = self.db.execute('''SELECT p.name, p.category_id, p.brand_id, p.supplier_id, 
                                          p.price, p.quantity, p.description 
                                          FROM products p WHERE p.product_id = ?''', (product_id,)).fetchone()
        
        # Переменные для выпадающих списков
        category_var = tk.StringVar()
        brand_var = tk.StringVar()
        supplier_var = tk.StringVar()
        
        # Поля формы
        form_frame = ttk.Frame(dialog)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Название
        ttk.Label(form_frame, text="Название товара:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(form_frame, width=40)
        name_entry.grid(row=0, column=1, pady=5, sticky=tk.W)
        
        # Категория
        ttk.Label(form_frame, text="Категория:").grid(row=1, column=0, sticky=tk.W, pady=5)
        category_combobox = ttk.Combobox(form_frame, textvariable=category_var, width=37)
        category_combobox['values'] = [f"{cat[0]} - {cat[1]}" for cat in categories]
        category_combobox.grid(row=1, column=1, pady=5, sticky=tk.W)
        
        # Бренд
        ttk.Label(form_frame, text="Бренд:").grid(row=2, column=0, sticky=tk.W, pady=5)
        brand_combobox = ttk.Combobox(form_frame, textvariable=brand_var, width=37)
        brand_combobox['values'] = [f"{brand[0]} - {brand[1]}" for brand in brands]
        brand_combobox.grid(row=2, column=1, pady=5, sticky=tk.W)
        
        # Поставщик
        ttk.Label(form_frame, text="Поставщик:").grid(row=3, column=0, sticky=tk.W, pady=5)
        supplier_combobox = ttk.Combobox(form_frame, textvariable=supplier_var, width=37)
        supplier_combobox['values'] = [f"{sup[0]} - {sup[1]}" for sup in suppliers]
        supplier_combobox.grid(row=3, column=1, pady=5, sticky=tk.W)
        
        # Цена и количество
        ttk.Label(form_frame, text="Цена:").grid(row=4, column=0, sticky=tk.W, pady=5)
        price_entry = ttk.Entry(form_frame, width=15)
        price_entry.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(form_frame, text="Количество:").grid(row=5, column=0, sticky=tk.W, pady=5)
        quantity_entry = ttk.Entry(form_frame, width=15)
        quantity_entry.grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # Описание
        ttk.Label(form_frame, text="Описание:").grid(row=6, column=0, sticky=tk.W, pady=5)
        description_text = tk.Text(form_frame, width=40, height=5, wrap=tk.WORD)
        description_text.grid(row=6, column=1, pady=5, sticky=tk.W)
        
        # Заполнение полей, если редактирование
        if product_data:
            name_entry.insert(0, product_data[0])
            
            for cat in categories:
                if cat[0] == product_data[1]:
                    category_var.set(f"{cat[0]} - {cat[1]}")
                    break
            
            for brand in brands:
                if brand[0] == product_data[2]:
                    brand_var.set(f"{brand[0]} - {brand[1]}")
                    break
            
            for sup in suppliers:
                if sup[0] == product_data[3]:
                    supplier_var.set(f"{sup[0]} - {sup[1]}")
                    break
            
            price_entry.insert(0, str(product_data[4]))
            quantity_entry.insert(0, str(product_data[5]))
            description_text.insert("1.0", product_data[6] if product_data[6] else "")
        
        # Кнопки
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def save_product():
            """Сохранение товара"""
            name = name_entry.get()
            category = category_var.get().split(" - ")[0]
            brand = brand_var.get().split(" - ")[0]
            supplier = supplier_var.get().split(" - ")[0]
            price = price_entry.get()
            quantity = quantity_entry.get()
            description = description_text.get("1.0", tk.END).strip()
            
            # Валидация данных
            if not all([name, category, brand, supplier, price, quantity]):
                messagebox.showerror("Ошибка", "Все поля обязательны для заполнения")
                return
            
            try:
                price = float(price)
                quantity = int(quantity)
                if price <= 0 or quantity < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Ошибка", "Цена и количество должны быть положительными числами")
                return
            
            try:
                if product_id:
                    # Обновление существующего товара
                    self.db.execute('''UPDATE products SET name=?, category_id=?, brand_id=?, supplier_id=?, 
                                    price=?, quantity=?, description=? WHERE product_id=?''',
                                    (name, category, brand, supplier, price, quantity, description, product_id))
                    message = "Товар успешно обновлен"
                else:
                    # Добавление нового товара
                    self.db.execute('''INSERT INTO products (name, category_id, brand_id, supplier_id, 
                                    price, quantity, description) 
                                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                                    (name, category, brand, supplier, price, quantity, description))
                    message = "Товар успешно добавлен"
                
                self.db.commit()
                dialog.destroy()
                self.update_products_list()
                messagebox.showinfo("Успех", message)
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка базы данных", f"Не удалось сохранить товар: {e}")
        
        ttk.Button(button_frame, text="Сохранить", command=save_product, style='Accent.TButton').pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Отмена", command=dialog.destroy).pack(side=tk.RIGHT)
    
    # ========== Методы для работы с клиентами ==========
    def update_customers_list(self):
        """Обновление списка клиентов"""
        self.customers_tree.delete(*self.customers_tree.get_children())
        customers = self.db.execute("SELECT * FROM customers").fetchall()
        for customer in customers:
            self.customers_tree.insert("", tk.END, values=customer)
    
    def search_customers(self):
        """Поиск клиентов"""
        query = self.customer_search_entry.get()
        if not query:
            self.update_customers_list()
            return
        
        self.customers_tree.delete(*self.customers_tree.get_children())
        customers = self.db.execute('''SELECT * FROM customers 
                                    WHERE first_name LIKE ? OR last_name LIKE ? OR phone LIKE ? OR email LIKE ?''',
                                    (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%")).fetchall()
        for customer in customers:
            self.customers_tree.insert("", tk.END, values=customer)
    
    def reset_customers_search(self):
        """Сброс поиска клиентов"""
        self.customer_search_entry.delete(0, tk.END)
        self.update_customers_list()
    
    def add_customer(self):
        """Добавление нового клиента"""
        self.customer_dialog("Добавить клиента")
    
    def edit_customer(self):
        """Редактирование клиента"""
        selected = self.customers_tree.focus()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите клиента для редактирования")
            return
        
        customer_id = self.customers_tree.item(selected)['values'][0]
        self.customer_dialog("Редактировать клиента", customer_id)
    
    def delete_customer(self):
        """Удаление клиента"""
        selected = self.customers_tree.focus()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите клиента для удаления")
            return
        
        customer_id = self.customers_tree.item(selected)['values'][0]
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этого клиента?"):
            self.db.execute("DELETE FROM customers WHERE customer_id = ?", (customer_id,))
            self.db.commit()
            self.update_customers_list()
            messagebox.showinfo("Успех", "Клиент успешно удален")
    
    def customer_dialog(self, title, customer_id=None):
        """Диалоговое окно для добавления/редактирования клиента"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        
        # Центрирование окна
        self.center_window(dialog)
        
        # Получение данных о клиенте, если редактирование
        customer_data = None
        if customer_id:
            customer_data = self.db.execute("SELECT * FROM customers WHERE customer_id = ?", (customer_id,)).fetchone()
        
        # Поля формы
        form_frame = ttk.Frame(dialog)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(form_frame, text="Имя:").grid(row=0, column=0, sticky=tk.W, pady=5)
        first_name_entry = ttk.Entry(form_frame, width=30)
        first_name_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(form_frame, text="Фамилия:").grid(row=1, column=0, sticky=tk.W, pady=5)
        last_name_entry = ttk.Entry(form_frame, width=30)
        last_name_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(form_frame, text="Телефон:").grid(row=2, column=0, sticky=tk.W, pady=5)
        phone_entry = ttk.Entry(form_frame, width=30)
        phone_entry.grid(row=2, column=1, pady=5)
        
        ttk.Label(form_frame, text="Email:").grid(row=3, column=0, sticky=tk.W, pady=5)
        email_entry = ttk.Entry(form_frame, width=30)
        email_entry.grid(row=3, column=1, pady=5)
        
        # Заполнение полей, если редактирование
        if customer_data:
            first_name_entry.insert(0, customer_data[1])
            last_name_entry.insert(0, customer_data[2])
            phone_entry.insert(0, customer_data[3] if customer_data[3] else "")
            email_entry.insert(0, customer_data[4] if customer_data[4] else "")
        
        # Кнопки
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def save_customer():
            """Сохранение клиента"""
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            phone = phone_entry.get()
            email = email_entry.get()
            
            if not first_name or not last_name:
                messagebox.showerror("Ошибка", "Имя и фамилия обязательны для заполнения")
                return
            
            try:
                if customer_id:
                    # Обновление существующего клиента
                    self.db.execute('''UPDATE customers SET first_name=?, last_name=?, phone=?, email=? 
                                    WHERE customer_id=?''',
                                    (first_name, last_name, phone, email, customer_id))
                    message = "Данные клиента обновлены"
                else:
                    # Добавление нового клиента
                    reg_date = datetime.now().strftime("%Y-%m-%d")
                    self.db.execute('''INSERT INTO customers (first_name, last_name, phone, email, registration_date) 
                                    VALUES (?, ?, ?, ?, ?)''',
                                    (first_name, last_name, phone, email, reg_date))
                    message = "Клиент успешно добавлен"
                
                self.db.commit()
                dialog.destroy()
                self.update_customers_list()
                messagebox.showinfo("Успех", message)
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка базы данных", f"Не удалось сохранить клиента: {e}")
        
        ttk.Button(button_frame, text="Сохранить", command=save_customer, style='Accent.TButton').pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Отмена", command=dialog.destroy).pack(side=tk.RIGHT)
    
    # ========== Методы для работы с заказами ==========
    def update_orders_list(self):
        """Обновление списка заказов"""
        self.orders_tree.delete(*self.orders_tree.get_children())
        orders = self.db.execute('''SELECT o.order_id, c.first_name || ' ' || c.last_name, 
                                 o.order_date, o.total_amount, o.status 
                                 FROM orders o 
                                 JOIN customers c ON o.customer_id = c.customer_id
                                 ORDER BY o.order_date DESC''').fetchall()
        
        for order in orders:
            self.orders_tree.insert("", tk.END, values=order)
    
    def filter_orders(self):
        """Фильтрация заказов"""
        status = self.status_filter.get()
        date_from = self.date_from_entry.get()
        date_to = self.date_to_entry.get()
        
        query = '''SELECT o.order_id, c.first_name || ' ' || c.last_name, 
                 o.order_date, o.total_amount, o.status 
                 FROM orders o 
                 JOIN customers c ON o.customer_id = c.customer_id'''
        
        conditions = []
        params = []
        
        if status != "Все":
            conditions.append("o.status = ?")
            params.append(status)
        
        if date_from:
            conditions.append("o.order_date >= ?")
            params.append(date_from)
        
        if date_to:
            conditions.append("o.order_date <= ?")
            params.append(date_to)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY o.order_date DESC"
        
        self.orders_tree.delete(*self.orders_tree.get_children())
        orders = self.db.execute(query, tuple(params)).fetchall()
        
        for order in orders:
            self.orders_tree.insert("", tk.END, values=order)
    
    def reset_orders_filter(self):
        """Сброс фильтров заказов"""
        self.status_filter.set("Все")
        self.date_from_entry.delete(0, tk.END)
        self.date_to_entry.delete(0, tk.END)
        self.update_orders_list()
    
    def create_order(self):
        """Создание нового заказа"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Новый заказ")
        dialog.geometry("900x700")
     
        # Центрирование окна
        self.center_window(dialog)
        
        # Переменные
        self.selected_products = {}  # Словарь для хранения выбранных товаров {product_id: [name, price, quantity]}
        
        # Выбор клиента
        customer_frame = ttk.Frame(dialog)
        customer_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(customer_frame, text="Клиент:", style='Header.TLabel').pack(anchor=tk.W)
        
        customer_var = tk.StringVar()
        customers = self.db.execute("SELECT customer_id, first_name || ' ' || last_name FROM customers").fetchall()
        customer_combobox = ttk.Combobox(customer_frame, textvariable=customer_var, width=40)
        customer_combobox['values'] = [f"{cust[0]} - {cust[1]}" for cust in customers]
        customer_combobox.pack(fill=tk.X, pady=5)
        
        # Разделитель
        ttk.Separator(dialog).pack(fill=tk.X, padx=10)
        
        # Товары
        products_frame = ttk.Frame(dialog)
        products_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Список доступных товаров
        ttk.Label(products_frame, text="Доступные товары:", style='Header.TLabel').grid(row=0, column=0, sticky=tk.W)
        
        columns = ("id", "name", "price", "quantity")
        self.products_order_tree = ttk.Treeview(products_frame, columns=columns, show="headings", height=10)
        
        self.products_order_tree.heading("id", text="ID", anchor=tk.CENTER)
        self.products_order_tree.heading("name", text="Название", anchor=tk.CENTER)
        self.products_order_tree.heading("price", text="Цена", anchor=tk.CENTER)
        self.products_order_tree.heading("quantity", text="Доступно", anchor=tk.CENTER)
        
        self.products_order_tree.column("id", width=50, anchor=tk.CENTER)
        self.products_order_tree.column("name", width=250, anchor=tk.W)
        self.products_order_tree.column("price", width=100, anchor=tk.E)
        self.products_order_tree.column("quantity", width=100, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(products_frame, orient=tk.VERTICAL, command=self.products_order_tree.yview)
        self.products_order_tree.configure(yscroll=scrollbar.set)
        
        self.products_order_tree.grid(row=1, column=0, sticky=tk.NSEW)
        scrollbar.grid(row=1, column=1, sticky=tk.NS)
        
        # Заполнение списка товаров
        products = self.db.execute('''SELECT p.product_id, p.name, p.price, p.quantity 
                                   FROM products p WHERE p.quantity > 0''').fetchall()
        for product in products:
            self.products_order_tree.insert("", tk.END, values=product)
        
        # Управление количеством
        quantity_frame = ttk.Frame(products_frame)
        quantity_frame.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        ttk.Label(quantity_frame, text="Количество:").pack(side=tk.LEFT)
        self.quantity_entry = ttk.Entry(quantity_frame, width=10)
        self.quantity_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(quantity_frame, text="Добавить", command=lambda: self.add_to_order(self.products_order_tree)).pack(side=tk.LEFT)
        
        # Разделитель
        ttk.Separator(dialog).pack(fill=tk.X, padx=10)
        
        # Выбранные товары
        selected_frame = ttk.Frame(dialog)
        selected_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(selected_frame, text="Выбранные товары:", style='Header.TLabel').grid(row=0, column=0, sticky=tk.W)
        
        selected_columns = ("id", "name", "price", "quantity", "sum")
        self.selected_order_tree = ttk.Treeview(selected_frame, columns=selected_columns, show="headings", height=10)
        
        self.selected_order_tree.heading("id", text="ID", anchor=tk.CENTER)
        self.selected_order_tree.heading("name", text="Название", anchor=tk.CENTER)
        self.selected_order_tree.heading("price", text="Цена", anchor=tk.CENTER)
        self.selected_order_tree.heading("quantity", text="Количество", anchor=tk.CENTER)
        self.selected_order_tree.heading("sum", text="Сумма", anchor=tk.CENTER)
        
        self.selected_order_tree.column("id", width=50, anchor=tk.CENTER)
        self.selected_order_tree.column("name", width=250, anchor=tk.W)
        self.selected_order_tree.column("price", width=100, anchor=tk.E)
        self.selected_order_tree.column("quantity", width=100, anchor=tk.CENTER)
        self.selected_order_tree.column("sum", width=100, anchor=tk.E)
        
        selected_scrollbar = ttk.Scrollbar(selected_frame, orient=tk.VERTICAL, command=self.selected_order_tree.yview)
        self.selected_order_tree.configure(yscroll=selected_scrollbar.set)
        
        self.selected_order_tree.grid(row=1, column=0, sticky=tk.NSEW)
        selected_scrollbar.grid(row=1, column=1, sticky=tk.NS)
        
        # Управление выбранными товарами
        selected_btn_frame = ttk.Frame(selected_frame)
        selected_btn_frame.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        ttk.Button(selected_btn_frame, text="Удалить", command=self.remove_from_order).pack(side=tk.LEFT, padx=3)
        ttk.Button(selected_btn_frame, text="Очистить", command=self.clear_order).pack(side=tk.LEFT, padx=3)
       
        # Итого
        total_frame = ttk.Frame(dialog)
        total_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.total_label = ttk.Label(total_frame, text="Итого: 0.00", style='Header.TLabel')
        self.total_label.pack(side=tk.RIGHT)
        
        # Кнопки сохранения/отмены
        
        def save_order():
            """Сохранение заказа в базу данных"""
            customer = customer_var.get()
            if not customer:
                messagebox.showerror("Ошибка", "Выберите клиента")
                return
            
            if not self.selected_products:
                messagebox.showerror("Ошибка", "Добавьте хотя бы один товар")
                return
            
            customer_id = customer.split(" - ")[0]
            
            # Расчет общей суммы
            total = sum(float(self.selected_order_tree.item(item)['values'][4]) 
                      for item in self.selected_order_tree.get_children())
            
            try:
                # Создание заказа
                order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.db.execute('''INSERT INTO orders (customer_id, order_date, total_amount, status) 
                                VALUES (?, ?, ?, ?)''',
                                (customer_id, order_date, total, "Новый"))
                order_id = self.db.execute("SELECT last_insert_rowid()").fetchone()[0]
                
                # Добавление товаров в заказ
                for item in self.selected_order_tree.get_children():
                    product_id, _, _, quantity, _ = self.selected_order_tree.item(item)['values']
                    price = float(self.selected_order_tree.item(item)['values'][2])
                    
                    self.db.execute('''INSERT INTO order_items (order_id, product_id, quantity, price) 
                                    VALUES (?, ?, ?, ?)''',
                                    (order_id, product_id, quantity, price))
                    
                    # Уменьшение количества товара на складе
                    self.db.execute('''UPDATE products SET quantity = quantity - ? 
                                    WHERE product_id = ?''', (quantity, product_id))
                
                self.db.commit()
                dialog.destroy()
                self.update_orders_list()
                messagebox.showinfo("Успех", f"Заказ #{order_id} успешно создан")
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка базы данных", f"Не удалось сохранить заказ: {e}")

        ttk.Button(selected_btn_frame, text="Отмена", command=dialog.destroy).pack(side=tk.RIGHT, padx= 3)
        ttk.Button(selected_btn_frame, text="Сохранить заказ", command=save_order).pack(side=tk.RIGHT, padx=3)
    
        
        # Настройка весов для растягивания
        products_frame.columnconfigure(0, weight=1)
        products_frame.rowconfigure(1, weight=1)
        selected_frame.columnconfigure(0, weight=1)
        selected_frame.rowconfigure(1, weight=1)
    
    def add_to_order(self, tree):
        """Добавление товара в заказ"""
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите товар для добавления")
            return
        
        try:
            quantity = int(self.quantity_entry.get())
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное количество (целое число > 0)")
            return
        
        product = tree.item(selected)['values']
        product_id = product[0]
        
        # Проверка доступного количества
        available = int(product[3])
        if quantity > available:
            messagebox.showerror("Ошибка", f"Доступно только {available} единиц товара")
            return
        
        # Проверка, не добавлен ли уже товар
        if product_id in self.selected_products:
            messagebox.showerror("Ошибка", "Этот товар уже добавлен в заказ")
            return
        
        # Добавление товара в заказ
        price = float(product[2])
        total = price * quantity
        self.selected_products[product_id] = [product[1], price, quantity]
        
        # Обновление таблицы выбранных товаров
        self.selected_order_tree.insert("", tk.END, 
                                     values=(product_id, product[1], price, quantity, total))
        
        # Обновление общей суммы
        self.update_order_total()
    
    def remove_from_order(self):
        """Удаление товара из заказа"""
        selected = self.selected_order_tree.focus()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите товар для удаления")
            return
        
        product_id = self.selected_order_tree.item(selected)['values'][0]
        del self.selected_products[product_id]
        self.selected_order_tree.delete(selected)
        self.update_order_total()
    
    def clear_order(self):
        """Очистка заказа"""
        if not self.selected_products:
            return
        
        if messagebox.askyesno("Подтверждение", "Очистить весь заказ?"):
            self.selected_products.clear()
            self.selected_order_tree.delete(*self.selected_order_tree.get_children())
            self.update_order_total()
    
    def update_order_total(self):
        """Обновление общей суммы заказа"""
        total = sum(float(self.selected_order_tree.item(item)['values'][4]) 
                  for item in self.selected_order_tree.get_children())
        self.total_label.config(text=f"Итого: {total:.2f}")
    
    def view_order(self):
        """Просмотр деталей заказа"""
        selected = self.orders_tree.focus()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите заказ для просмотра")
            return
        
        order_id = self.orders_tree.item(selected)['values'][0]
        order_data = self.db.execute('''SELECT o.order_id, c.first_name || ' ' || c.last_name, 
                                     o.order_date, o.total_amount, o.status 
                                     FROM orders o 
                                     JOIN customers c ON o.customer_id = c.customer_id
                                     WHERE o.order_id = ?''', (order_id,)).fetchone()
        
        items = self.db.execute('''SELECT p.product_id, p.name, oi.quantity, oi.price, oi.quantity * oi.price 
                                FROM order_items oi 
                                JOIN products p ON oi.product_id = p.product_id 
                                WHERE oi.order_id = ?''', (order_id,)).fetchall()
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Заказ #{order_id}")
        dialog.geometry("700x500")
        
        # Центрирование окна
        self.center_window(dialog)
        
        # Информация о заказе
        info_frame = ttk.Frame(dialog)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(info_frame, text=f"Заказ #{order_data[0]}", style='Header.TLabel').grid(row=0, column=0, sticky=tk.W)
        ttk.Label(info_frame, text=f"Клиент: {order_data[1]}").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(info_frame, text=f"Дата: {order_data[2]}").grid(row=2, column=0, sticky=tk.W)
        
        # Статус с цветом
        status_frame = ttk.Frame(info_frame)
        status_frame.grid(row=3, column=0, sticky=tk.W)
        ttk.Label(status_frame, text="Статус:").pack(side=tk.LEFT)
        
        status_style = f"Status.{order_data[4]}.TLabel"
        ttk.Label(status_frame, text=order_data[4], style=status_style).pack(side=tk.LEFT)
        
        ttk.Label(info_frame, text=f"Общая сумма: {order_data[3]:.2f}").grid(row=4, column=0, sticky=tk.W)
        
        # Товары в заказе
        ttk.Label(dialog, text="Товары:", style='Header.TLabel').pack(anchor=tk.W, padx=10, pady=(10, 0))
        
        columns = ("id", "name", "quantity", "price", "sum")
        tree = ttk.Treeview(dialog, columns=columns, show="headings")
        
        tree.heading("id", text="ID", anchor=tk.CENTER)
        tree.heading("name", text="Название", anchor=tk.CENTER)
        tree.heading("quantity", text="Количество", anchor=tk.CENTER)
        tree.heading("price", text="Цена", anchor=tk.CENTER)
        tree.heading("sum", text="Сумма", anchor=tk.CENTER)
        
        tree.column("id", width=50, anchor=tk.CENTER)
        tree.column("name", width=250, anchor=tk.W)
        tree.column("quantity", width=100, anchor=tk.CENTER)
        tree.column("price", width=100, anchor=tk.E)
        tree.column("sum", width=100, anchor=tk.E)
        
        scrollbar = ttk.Scrollbar(dialog, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        for item in items:
            tree.insert("", tk.END, values=item)
        
        # Кнопка закрытия
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Закрыть", command=dialog.destroy, style='Accent.TButton').pack(side=tk.RIGHT)
    
    def update_order_status(self):
        """Изменение статуса заказа"""
        selected = self.orders_tree.focus()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите заказ для изменения статуса")
            return
        
        order_id = self.orders_tree.item(selected)['values'][0]
        current_status = self.orders_tree.item(selected)['values'][4]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Изменение статуса заказа")
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        
        # Центрирование окна
        self.center_window(dialog)
        
        ttk.Label(dialog, text=f"Заказ #{order_id}", style='Header.TLabel').pack(pady=5)
        
        status_frame = ttk.Frame(dialog)
        status_frame.pack(pady=5)
        
        ttk.Label(status_frame, text="Текущий статус:").pack(side=tk.LEFT)
        
        status_style = f"Status.{current_status}.TLabel"
        ttk.Label(status_frame, text=current_status, style=status_style).pack(side=tk.LEFT)
        
        ttk.Label(dialog, text="Новый статус:").pack()
        
        status_var = tk.StringVar(value=current_status)
        status_combobox = ttk.Combobox(dialog, textvariable=status_var, 
                                      values=["Новый", "В обработке", "Выполнен", "Отменен"])
        status_combobox.pack(pady=5)
        
        def save_status():
            """Сохранение нового статуса"""
            new_status = status_var.get()
            if new_status == current_status:
                messagebox.showinfo("Информация", "Статус не изменен")
                dialog.destroy()
                return
            
            try:
                self.db.execute("UPDATE orders SET status = ? WHERE order_id = ?", (new_status, order_id))
                self.db.commit()
                dialog.destroy()
                self.update_orders_list()
                messagebox.showinfo("Успех", "Статус заказа обновлен")
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка базы данных", f"Не удалось обновить статус: {e}")
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Сохранить", command=save_status).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT, padx=10)
  
    def setup_reports_tab(self):
        # Основной фрейм для отчетов
        main_frame = ttk.Frame(self.reports_tab)
        main_frame.pack(fill=BOTH, expand=1, padx=5, pady=5)
        
        # Фрейм для кнопок отчетов
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=X, pady=(0, 5))
        
        ttk.Button(btn_frame, text="Товары на складе", command=self.show_inventory_report).pack(side=LEFT, padx=30)
        ttk.Button(btn_frame, text="Продажи по категориям", command=self.show_sales_by_category_report).pack(side=LEFT, padx=30)
        ttk.Button(btn_frame, text="Топ клиентов", command=self.show_top_customers_report).pack(side=LEFT, padx=30)
        ttk.Button(btn_frame, text="Статистика заказов", command=self.show_orders_stats_report).pack(side=LEFT, padx=30)
        ttk.Button(btn_frame, text="Товары с низким остатком", command=self.show_few_orders_report).pack(side=LEFT, padx=30)
        ttk.Button(btn_frame, text="Средний чек по месяцам", command=self.show_avg_bill_report).pack(side=LEFT, padx=30)

        # Treeview для отображения отчетов
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=BOTH, expand=1)
        
        scroll_y = ttk.Scrollbar(tree_frame)
        scroll_y.pack(side=RIGHT, fill=Y)
        
        scroll_x = ttk.Scrollbar(tree_frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        
        self.report_tree = ttk.Treeview(tree_frame, show='headings', yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.report_tree.pack(fill=BOTH, expand=1)
        
        scroll_y.config(command=self.report_tree.yview)
        scroll_x.config(command=self.report_tree.xview)
    


    def show_inventory_report(self):
        # Очищаем treeview
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
        
        # Настраиваем колонки
        self.report_tree['columns'] = ('Товар', 'Категория', 'Количество', 'Цена')
        for col in self.report_tree['columns']:
            self.report_tree.heading(col, text=col)
        
        # Подключаемся к базе данных
        conn = sqlite3.connect('sport_store.db')
        cursor = conn.cursor()
        
        # Выполняем запрос
        cursor.execute('''SELECT p.name, c.name, p.quantity, p.price 
                       FROM products p 
                       JOIN categories c ON p.category_id = c.category_id 
                       ORDER BY p.quantity''')
        
        # Добавляем данные
        for row in cursor.fetchall():
            self.report_tree.insert('', END, values=row)
        
        conn.close()
       
    
    def show_sales_by_category_report(self):
        # Очищаем treeview
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
        
        # Настраиваем колонки
        self.report_tree['columns'] = ('Категория', 'Количество продаж', 'Общая сумма')
        for col in self.report_tree['columns']:
            self.report_tree.heading(col, text=col)
        
        # Подключаемся к базе данных
        conn = sqlite3.connect('sport_store.db')
        cursor = conn.cursor()
        
        # Выполняем запрос
        cursor.execute('''SELECT c.name, SUM(oi.quantity), SUM(oi.quantity * oi.price) 
                       FROM order_items oi 
                       JOIN products p ON oi.product_id = p.product_id 
                       JOIN categories c ON p.category_id = c.category_id 
                       GROUP BY c.name 
                       ORDER BY SUM(oi.quantity * oi.price) DESC''')
        
        # Добавляем данные
        for row in cursor.fetchall():
            self.report_tree.insert('', END, values=row)
        
        conn.close()
       
    
    def show_top_customers_report(self):
        # Очищаем treeview
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
        
        # Настраиваем колонки
        self.report_tree['columns'] = ('Клиент', 'Количество заказов', 'Общая сумма')
        for col in self.report_tree['columns']:
            self.report_tree.heading(col, text=col)
        
        # Подключаемся к базе данных
        conn = sqlite3.connect('sport_store.db')
        cursor = conn.cursor()
        
        # Выполняем запрос
        cursor.execute('''SELECT c.first_name || ' ' || c.last_name, COUNT(o.order_id), SUM(o.total_amount) 
                       FROM orders o 
                       JOIN customers c ON o.customer_id = c.customer_id 
                       GROUP BY c.customer_id 
                       ORDER BY SUM(o.total_amount) DESC 
                       LIMIT 10''')
        
        # Добавляем данные
        for row in cursor.fetchall():
            self.report_tree.insert('', END, values=row)
        
        conn.close()
        
    
    def show_orders_stats_report(self):
        # Очищаем treeview
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
        
        # Настраиваем колонки
        self.report_tree['columns'] = ('Показатель', 'Значение')
        for col in self.report_tree['columns']:
            self.report_tree.heading(col, text=col)
        
        # Подключаемся к базе данных
        conn = sqlite3.connect('sport_store.db')
        cursor = conn.cursor()
        
        # Выполняем запросы и добавляем данные
        cursor.execute("SELECT COUNT(*) FROM orders")
        total_orders = cursor.fetchone()[0]
        self.report_tree.insert('', END, values=('Всего заказов', total_orders))
        
        cursor.execute("SELECT SUM(total_amount) FROM orders")
        total_sales = cursor.fetchone()[0]
        self.report_tree.insert('', END, values=('Общий объем продаж', f"{total_sales:.2f} руб."))
        
        cursor.execute("SELECT AVG(total_amount) FROM orders")
        avg_order = cursor.fetchone()[0]
        self.report_tree.insert('', END, values=('Средний чек', f"{avg_order:.2f} руб."))
        
        cursor.execute("SELECT COUNT(DISTINCT customer_id) FROM orders")
        unique_customers = cursor.fetchone()[0]
        self.report_tree.insert('', END, values=('Уникальных клиентов', unique_customers))

    def show_few_orders_report(self):
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)

        self.report_tree['columns'] = ('Товар', 'Количество', 'Цена')
        for col in self.report_tree['columns']:
            self.report_tree.heading(col, text=col)
    
        conn = sqlite3.connect('sport_store.db')
        cursor = conn.cursor()
        cursor.execute("""SELECT name, quantity, price
                        FROM products
                        WHERE quantity < 5
                        ORDER BY quantity ASC;""")
        for row in cursor.fetchall():
            self.report_tree.insert('', END, values=row)
        
        conn.close()

    def show_avg_bill_report(self):
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)

        self.report_tree['columns'] = ('Месяц','Средний чек')
        for col in self.report_tree['columns']:
            self.report_tree.heading(col, text=col)
    
        conn = sqlite3.connect('sport_store.db')
        cursor = conn.cursor()
        #средний чек по месяцам
        cursor.execute("""SELECT 
    CASE strftime('%m', order_date) 
        WHEN '01' THEN 'Январь'
        WHEN '02' THEN 'Февраль'
        WHEN '03' THEN 'Март'
        WHEN '04' THEN 'Апрель'
        WHEN '05' THEN 'Май'
        WHEN '06' THEN 'Июнь'
        WHEN '07' THEN 'Июль'
        WHEN '08' THEN 'Август'
        WHEN '09' THEN 'Сентябрь'
        WHEN '10' THEN 'Октябрь'
        WHEN '11' THEN 'Ноябрь'
        WHEN '12' THEN 'Декабрь'
    END AS month_name,
    ROUND(AVG(total_amount)) AS avg_order_value
    FROM orders
    GROUP BY strftime('%m', order_date)
    ORDER BY strftime('%m', order_date); """)
        
        for row in cursor.fetchall():
            self.report_tree.insert('', END, values=row)
        
        conn.close()
    # ========== Вспомогательные методы ==========
    def center_window(self, window):
        """Центрирование окна на экране"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')
    
    def __del__(self):
        """Закрытие соединения с БД при уничтожении объекта"""
        self.db.close()

