import mysql.connector
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
from db_config import DB_CONFIG, DB_NAME
import json

class ModernAdminPanel:
    def __init__(self, root):
        self.root = root
        self.root.title('Админ-панель каршеринга')
        self.root.geometry('1200x800')
        self.root.configure(bg='#1a1a1a')
        
        self.setup_styles()
        
        self.create_main_interface()
        
        self.refresh_all_data()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Title.TLabel', background='#1a1a1a', foreground='#ffffff', 
                       font=('Segoe UI', 20, 'bold'))
        style.configure('Header.TLabel', background='#1a1a1a', foreground='#ffffff', 
                       font=('Segoe UI', 14, 'bold'))
        style.configure('Info.TLabel', background='#1a1a1a', foreground='#cccccc', 
                       font=('Segoe UI', 11))

        style.configure('Modern.Treeview', 
                       background='#2d2d2d', 
                       foreground='#ffffff',
                       fieldbackground='#2d2d2d',
                       borderwidth=0,
                       rowheight=30,
                       font=('Segoe UI', 10))
        style.configure('Modern.Treeview.Heading', 
                       background='#1a1a1a',
                       foreground='#ffffff',
                       font=('Segoe UI', 11, 'bold'),
                       borderwidth=1,
                       relief='solid')
        style.map('Modern.Treeview', 
                 background=[('selected', '#ffffff')],
                 foreground=[('selected', '#1a1a1a')])
        
        style.configure('Modern.TButton',
                       background='#ffffff',
                       foreground='#1a1a1a',
                       font=('Segoe UI', 10, 'bold'),
                       borderwidth=0,
                       padding=(10, 5))
        style.map('Modern.TButton',
                 background=[('active', '#f0f0f0')])
        
        style.configure('Modern.TNotebook', background='#1a1a1a', borderwidth=0)
        style.configure('Modern.TNotebook.Tab', 
                       background='#2d2d2d',
                       foreground='#ffffff',
                       padding=(20, 10),
                       font=('Segoe UI', 11))
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', '#ffffff')],
                 foreground=[('selected', '#1a1a1a')])
    
    def create_main_interface(self):

        title_frame = tk.Frame(self.root, bg='#1a1a1a', height=80)
        title_frame.pack(fill='x', padx=20, pady=10)
        title_frame.pack_propagate(False)
        
        title_label = ttk.Label(title_frame, text='Админ-панель каршеринга', 
                               style='Title.TLabel')
        title_label.pack(side='left', pady=20)
        
  
        refresh_btn = ttk.Button(title_frame, text='🔄 Обновить все', 
                                style='Modern.TButton',
                                command=self.refresh_all_data)
        refresh_btn.pack(side='right', pady=20)
        

        self.create_stats_panel()
        
        # Создание вкладок
        self.notebook = ttk.Notebook(self.root, style='Modern.TNotebook')
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Вкладка заказов
        self.create_orders_tab()
        
        # Вкладка пользователей
        self.create_users_tab()
        
        # Вкладка машин
        self.create_cars_tab()
        
        # Вкладка аналитики
        self.create_analytics_tab()
    
    def create_stats_panel(self):
        stats_frame = tk.Frame(self.root, bg='#2d2d2d', height=100)
        stats_frame.pack(fill='x', padx=20, pady=10)
        stats_frame.pack_propagate(False)
        
    
        self.stats_cards = {}
        card_titles = ['Всего заказов', 'Активных заказов', 'Пользователей', 'Машин']
        card_keys = ['total_orders', 'active_orders', 'total_users', 'total_cars']
        
        for i, (title, key) in enumerate(zip(card_titles, card_keys)):
            card = tk.Frame(stats_frame, bg='#3d3d3d', relief='raised', bd=1)
            card.place(x=i*280+20, y=10, width=250, height=80)
            
            value_label = ttk.Label(card, text='0', font=('Segoe UI', 24, 'bold'),
                                   background='#3d3d3d', foreground='#ffffff')
            value_label.pack(pady=5)
            
            title_label = ttk.Label(card, text=title, font=('Segoe UI', 11),
                                   background='#3d3d3d', foreground='#ffffff')
            title_label.pack()
            
            self.stats_cards[key] = value_label
    
    def create_orders_tab(self):
        orders_frame = ttk.Frame(self.notebook)
        self.notebook.add(orders_frame, text='📋 Заказы')
    
        control_frame = tk.Frame(orders_frame, bg='#1a1a1a')
        control_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(control_frame, text='✅ Завершить заказ', 
                  style='Modern.TButton',
                  command=self.complete_order).pack(side='left', padx=5)
        ttk.Button(control_frame, text='❌ Отменить заказ', 
                  style='Modern.TButton',
                  command=self.cancel_order).pack(side='left', padx=5)
        

        self.orders_tree = ttk.Treeview(orders_frame, style='Modern.Treeview',
                                       columns=('ID', 'Пользователь', 'Машина', 'Номер', 
                                               'Начало', 'Конец', 'Статус', 'Длительность'),
                                       show='headings')
        
 
        columns_config = {
            'ID': 50, 'Пользователь': 120, 'Машина': 140, 'Номер': 100,
            'Начало': 130, 'Конец': 130, 'Статус': 100, 'Длительность': 120
        }
        
        for col, width in columns_config.items():
            self.orders_tree.heading(col, text=col)
            self.orders_tree.column(col, width=width, anchor='center')
        
   
        orders_scroll = ttk.Scrollbar(orders_frame, orient='vertical', 
                                     command=self.orders_tree.yview)
        self.orders_tree.configure(yscrollcommand=orders_scroll.set)
        
        self.orders_tree.pack(side='left', fill='both', expand=True, padx=10, pady=5)
        orders_scroll.pack(side='right', fill='y', pady=5)
    
    def create_users_tab(self):
        users_frame = ttk.Frame(self.notebook)
        self.notebook.add(users_frame, text='👥 Пользователи')
        
  
        control_frame = tk.Frame(users_frame, bg='#1a1a1a')
        control_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(control_frame, text='➕ Добавить пользователя', 
                  style='Modern.TButton',
                  command=self.add_user).pack(side='left', padx=5)
        ttk.Button(control_frame, text='✏️ Редактировать', 
                  style='Modern.TButton',
                  command=self.edit_user).pack(side='left', padx=5)
        ttk.Button(control_frame, text='🗑️ Удалить пользователя', 
                  style='Modern.TButton',
                  command=self.delete_user).pack(side='left', padx=5)
        
  
        self.users_tree = ttk.Treeview(users_frame, style='Modern.Treeview',
                                      columns=('ID', 'Имя пользователя', 'Email', 
                                              'Дата регистрации', 'Кол-во заказов'),
                                      show='headings')
        
        users_columns = {
            'ID': 50, 'Имя пользователя': 150, 'Email': 200,
            'Дата регистрации': 150, 'Кол-во заказов': 130
        }
        
        for col, width in users_columns.items():
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=width, anchor='center')
        
   
        users_scroll = ttk.Scrollbar(users_frame, orient='vertical', 
                                    command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=users_scroll.set)
        
        self.users_tree.pack(side='left', fill='both', expand=True, padx=10, pady=5)
        users_scroll.pack(side='right', fill='y', pady=5)
    
    def create_cars_tab(self):
        cars_frame = ttk.Frame(self.notebook)
        self.notebook.add(cars_frame, text='🚗 Машины')
        
 
        control_frame = tk.Frame(cars_frame, bg='#1a1a1a')
        control_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(control_frame, text='➕ Добавить машину', 
                  style='Modern.TButton',
                  command=self.add_car).pack(side='left', padx=5)
        ttk.Button(control_frame, text='🔧 Изменить статус', 
                  style='Modern.TButton',
                  command=self.change_car_status).pack(side='left', padx=5)
        ttk.Button(control_frame, text='✏️ Редактировать', 
                  style='Modern.TButton',
                  command=self.edit_car).pack(side='left', padx=5)
        ttk.Button(control_frame, text='🗑️ Удалить машину', 
                  style='Modern.TButton',
                  command=self.delete_car).pack(side='left', padx=5)
        

        self.cars_tree = ttk.Treeview(cars_frame, style='Modern.Treeview',
                                     columns=('ID', 'Модель', 'Номер', 'Статус', 
                                             'Цена/час', 'Заказов'),
                                     show='headings')
        
        cars_columns = {
            'ID': 50, 'Модель': 180, 'Номер': 120, 'Статус': 120,
            'Цена/час': 100, 'Заказов': 100
        }
        
        for col, width in cars_columns.items():
            self.cars_tree.heading(col, text=col)
            self.cars_tree.column(col, width=width, anchor='center')
        
     
        cars_scroll = ttk.Scrollbar(cars_frame, orient='vertical', 
                                   command=self.cars_tree.yview)
        self.cars_tree.configure(yscrollcommand=cars_scroll.set)
        
        self.cars_tree.pack(side='left', fill='both', expand=True, padx=10, pady=5)
        cars_scroll.pack(side='right', fill='y', pady=5)
    
    def create_analytics_tab(self):
        analytics_frame = ttk.Frame(self.notebook)
        self.notebook.add(analytics_frame, text='📊 Аналитика')
        
        
        self.analytics_text = tk.Text(analytics_frame, bg='#2d2d2d', fg='#ffffff',
                                     font=('Consolas', 11), wrap='word')
        self.analytics_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        analytics_scroll = ttk.Scrollbar(analytics_frame, orient='vertical',
                                        command=self.analytics_text.yview)
        self.analytics_text.configure(yscrollcommand=analytics_scroll.set)
        analytics_scroll.pack(side='right', fill='y', pady=10)
    
    def get_db_connection(self):
        config = DB_CONFIG.copy()
        config['database'] = DB_NAME
        return mysql.connector.connect(**config)
    
    def refresh_all_data(self):
        try:
            self.refresh_orders()
            self.refresh_users()
            self.refresh_cars()
            self.refresh_stats()
            self.refresh_analytics()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка обновления данных: {e}")
    
    def refresh_orders(self):
        for row in self.orders_tree.get_children():
            self.orders_tree.delete(row)
        
        cnx = self.get_db_connection()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("""
            SELECT o.id, u.username, c.model, c.number, o.start_time, o.end_time, o.status
            FROM orders o
            JOIN users u ON o.user_id = u.id
            JOIN cars c ON o.car_id = c.id
            ORDER BY o.start_time DESC
        """)
        orders = cursor.fetchall()
        
        for order in orders:
          
            if order['end_time']:
                duration = order['end_time'] - order['start_time']
                duration_str = str(duration).split('.')[0]  
            else:
                duration = datetime.now() - order['start_time']
                duration_str = f"{str(duration).split('.')[0]} (активно)"
            
            self.orders_tree.insert('', 'end', values=(
                order['id'], order['username'], order['model'], order['number'],
                order['start_time'].strftime('%Y-%m-%d %H:%M'),
                order['end_time'].strftime('%Y-%m-%d %H:%M') if order['end_time'] else '-',
                order['status'], duration_str
            ))
        
        cursor.close()
        cnx.close()
    
    def refresh_users(self):
        for row in self.users_tree.get_children():
            self.users_tree.delete(row)
        
        cnx = self.get_db_connection()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.id, u.username, u.email, u.created_at,
                   COUNT(o.id) as order_count
            FROM users u
            LEFT JOIN orders o ON u.id = o.user_id
            GROUP BY u.id
            ORDER BY u.created_at DESC
        """)
        users = cursor.fetchall()
        
        for user in users:
            self.users_tree.insert('', 'end', values=(
                user['id'], user['username'], user['email'],
                user['created_at'].strftime('%Y-%m-%d'),
                user['order_count']
            ))
        
        cursor.close()
        cnx.close()
    
    def refresh_cars(self):
        for row in self.cars_tree.get_children():
            self.cars_tree.delete(row)
        
        cnx = self.get_db_connection()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.id, c.model, c.number, c.status, c.price_per_hour,
                   COUNT(o.id) as order_count
            FROM cars c
            LEFT JOIN orders o ON c.id = o.car_id
            GROUP BY c.id
            ORDER BY c.model
        """)
        cars = cursor.fetchall()
        
        for car in cars:
     
            status_display = car['status']
            if car['status'] == 'available':
                status_display = '✅ Доступна'
            elif car['status'] == 'booked':
                status_display = '🔒 Забронирована'
            elif car['status'] == 'maintenance':
                status_display = '🔧 Обслуживание'
            
            self.cars_tree.insert('', 'end', values=(
                car['id'], car['model'], car['number'], status_display,
                f"{car['price_per_hour']} ₽", car['order_count']
            ))
        
        cursor.close()
        cnx.close()
    
    def refresh_stats(self):
        cnx = self.get_db_connection()
        cursor = cnx.cursor(dictionary=True)
        

        cursor.execute("SELECT COUNT(*) as count FROM orders")
        total_orders = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'active'")
        active_orders = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM users")
        total_users = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM cars")
        total_cars = cursor.fetchone()['count']
        
   
        self.stats_cards['total_orders'].config(text=str(total_orders))
        self.stats_cards['active_orders'].config(text=str(active_orders))
        self.stats_cards['total_users'].config(text=str(total_users))
        self.stats_cards['total_cars'].config(text=str(total_cars))
        
        cursor.close()
        cnx.close()
    
    def refresh_analytics(self):
        cnx = self.get_db_connection()
        cursor = cnx.cursor(dictionary=True)
        
        analytics_text = "📊 АНАЛИТИКА КАРШЕРИНГА\n"
        analytics_text += "=" * 50 + "\n\n"
        
 
        cursor.execute("""
            SELECT c.model, COUNT(o.id) as orders, 
                   SUM(CASE WHEN o.status = 'active' THEN 1 ELSE 0 END) as active_orders
            FROM cars c
            LEFT JOIN orders o ON c.id = o.car_id
            GROUP BY c.id
            ORDER BY orders DESC
        """)
        cars_stats = cursor.fetchall()
        
        analytics_text += "🚗 ПОПУЛЯРНОСТЬ МАШИН:\n"
        for car in cars_stats:
            analytics_text += f"   {car['model']}: {car['orders']} заказов "
            analytics_text += f"(активных: {car['active_orders']})\n"
        
       
        cursor.execute("""
            SELECT u.username, COUNT(o.id) as orders
            FROM users u
            LEFT JOIN orders o ON u.id = o.user_id
            GROUP BY u.id
            HAVING orders > 0
            ORDER BY orders DESC
            LIMIT 5
        """)
        top_users = cursor.fetchall()
        
        analytics_text += f"\n👑 ТОП-{len(top_users)} ПОЛЬЗОВАТЕЛЕЙ:\n"
        for i, user in enumerate(top_users, 1):
            analytics_text += f"   {i}. {user['username']}: {user['orders']} заказов\n"
        

        cursor.execute("""
            SELECT DATE(start_time) as order_date, COUNT(*) as orders
            FROM orders
            WHERE start_time >= DATE_SUB(NOW(), INTERVAL 7 DAY)
            GROUP BY DATE(start_time)
            ORDER BY order_date DESC
        """)
        daily_stats = cursor.fetchall()
        
        analytics_text += "\n📅 ЗАКАЗЫ ЗА ПОСЛЕДНИЕ 7 ДНЕЙ:\n"
        for day in daily_stats:
            analytics_text += f"   {day['order_date']}: {day['orders']} заказов\n"
        
    
        cursor.execute("""
            SELECT SUM(c.price_per_hour * 
                      TIMESTAMPDIFF(HOUR, o.start_time, 
                                   COALESCE(o.end_time, NOW()))) as revenue
            FROM orders o
            JOIN cars c ON o.car_id = c.id
            WHERE o.status IN ('completed', 'active')
        """)
        revenue = cursor.fetchone()['revenue'] or 0
        
        analytics_text += f"\n💰 ОБЩИЙ ДОХОД: {revenue:.2f} ₽\n"
        
     
        cursor.execute("""
            SELECT AVG(TIMESTAMPDIFF(HOUR, start_time, end_time)) as avg_duration
            FROM orders
            WHERE end_time IS NOT NULL
        """)
        avg_duration = cursor.fetchone()['avg_duration'] or 0
        
        analytics_text += f"⏱️ СРЕДНЯЯ ДЛИТЕЛЬНОСТЬ: {avg_duration:.1f} часов\n"
        
        self.analytics_text.delete('1.0', tk.END)
        self.analytics_text.insert('1.0', analytics_text)
        
        cursor.close()
        cnx.close()
    
  
    def complete_order(self):
        selected = self.orders_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите заказ для завершения")
            return
        
        order_id = self.orders_tree.item(selected[0])['values'][0]
        
        cnx = self.get_db_connection()
        cursor = cnx.cursor()
        
   
        cursor.execute("""
            UPDATE orders SET status = 'completed', end_time = NOW() 
            WHERE id = %s AND status = 'active'
        """, (order_id,))
        
        cursor.execute("""
            UPDATE cars SET status = 'available' 
            WHERE id = (SELECT car_id FROM orders WHERE id = %s)
        """, (order_id,))
        
        cnx.commit()
        cursor.close()
        cnx.close()
        
        messagebox.showinfo("Успех", "Заказ успешно завершен!")
        self.refresh_all_data()
    
    def cancel_order(self):
        selected = self.orders_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите заказ для отмены")
            return
        
        order_id = self.orders_tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите отменить заказ?"):
            cnx = self.get_db_connection()
            cursor = cnx.cursor()
            
            cursor.execute("""
                UPDATE orders SET status = 'cancelled', end_time = NOW() 
                WHERE id = %s
            """, (order_id,))
            
            cursor.execute("""
                UPDATE cars SET status = 'available' 
                WHERE id = (SELECT car_id FROM orders WHERE id = %s)
            """, (order_id,))
            
            cnx.commit()
            cursor.close()
            cnx.close()
            
            messagebox.showinfo("Успех", "Заказ отменен!")
            self.refresh_all_data()
    

    def add_user(self):
        messagebox.showinfo("Функция", "Добавление пользователя - в разработке")
    
    def edit_user(self):
        messagebox.showinfo("Функция", "Редактирование пользователя - в разработке")
    
    def delete_user(self):
        messagebox.showinfo("Функция", "Удаление пользователя - в разработке")
    
    def add_car(self):
        messagebox.showinfo("Функция", "Добавление машины - в разработке")
    
    def edit_car(self):
        messagebox.showinfo("Функция", "Редактирование машины - в разработке")
    
    def delete_car(self):
        messagebox.showinfo("Функция", "Удаление машины - в разработке")
    
    def change_car_status(self):
        selected = self.cars_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите машину")
            return
        
        car_id = self.cars_tree.item(selected[0])['values'][0]
        
    
        cnx = self.get_db_connection()
        cursor = cnx.cursor()
        cursor.execute("UPDATE cars SET status = 'maintenance' WHERE id = %s", (car_id,))
        cnx.commit()
        cursor.close()
        cnx.close()
        
        messagebox.showinfo("Успех", "Статус машины изменен на 'Обслуживание'")
        self.refresh_all_data()

def main():
    root = tk.Tk()
    app = ModernAdminPanel(root)
    root.mainloop()

if __name__ == '__main__':
    main()
