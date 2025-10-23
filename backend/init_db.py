import mysql.connector
from mysql.connector import errorcode
from db_config import DB_CONFIG, DB_NAME

TABLES = {}
TABLES['users'] = (
    "CREATE TABLE IF NOT EXISTS users ("
    "  id INT AUTO_INCREMENT PRIMARY KEY,"
    "  username VARCHAR(50) NOT NULL UNIQUE,"
    "  password VARCHAR(255) NOT NULL,"
    "  email VARCHAR(100) NOT NULL UNIQUE,"
    "  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    ") ENGINE=InnoDB"
)
TABLES['cars'] = (
    "CREATE TABLE IF NOT EXISTS cars ("
    "  id INT AUTO_INCREMENT PRIMARY KEY,"
    "  model VARCHAR(100) NOT NULL,"
    "  number VARCHAR(20) NOT NULL UNIQUE,"
    "  status ENUM('available','booked','maintenance') DEFAULT 'available',"
    "  price_per_hour DECIMAL(6,2) NOT NULL,"
    "  image_url VARCHAR(500)"
    ") ENGINE=InnoDB"
)
TABLES['orders'] = (
    "CREATE TABLE IF NOT EXISTS orders ("
    "  id INT AUTO_INCREMENT PRIMARY KEY,"
    "  user_id INT NOT NULL,"
    "  car_id INT NOT NULL,"
    "  start_time DATETIME NOT NULL,"
    "  end_time DATETIME,"
    "  status ENUM('active','completed','cancelled') DEFAULT 'active',"
    "  FOREIGN KEY (user_id) REFERENCES users(id),"
    "  FOREIGN KEY (car_id) REFERENCES cars(id)"
    ") ENGINE=InnoDB"
)

def create_database(cursor):
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8'")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)

def create_tables(cursor):
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print(f"Creating table {table_name}: ", end='')
            cursor.execute(table_description)
            print("OK")
        except mysql.connector.Error as err:
            print(f"Failed creating table {table_name}: {err}")

def insert_test_data(cursor):
    # Users
    users = [
        ("user1", "pass1", "user1@mail.com"),
        ("user2", "pass2", "user2@mail.com"),
        ("admin", "adminpass", "admin@mail.com")
    ]
    for u in users:
        cursor.execute("INSERT IGNORE INTO users (username, password, email) VALUES (%s, %s, %s)", u)
    # Cars
    cars = [
        ("Tesla Model 3", "A111AA", 15.00, "https://images.unsplash.com/photo-1617788138017-80ad40651399?w=400"),
        ("BMW i3", "B222BB", 12.50, "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=400"),
        ("Kia Rio", "C333CC", 8.00, "https://images.unsplash.com/photo-1502877338535-766e1452684a?w=400"),
        ("Mercedes C-Class", "D444DD", 18.00, "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=400"),
        ("Toyota Camry", "E555EE", 10.00, "https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?w=400")
    ]
    for c in cars:
        cursor.execute("INSERT IGNORE INTO cars (model, number, price_per_hour, image_url) VALUES (%s, %s, %s, %s)", c)
    # Orders
    orders = [
        (1, 1, '2025-10-17 10:00:00', '2025-10-17 12:00:00', 'completed'),
        (2, 2, '2025-10-17 13:00:00', None, 'active')
    ]
    for o in orders:
        cursor.execute("INSERT IGNORE INTO orders (user_id, car_id, start_time, end_time, status) VALUES (%s, %s, %s, %s, %s)", o)

def main():
    cnx = None
    cursor = None
    try:
        print("Попытка подключения к MySQL...")
        print(f"Хост: {DB_CONFIG['host']}, Пользователь: {DB_CONFIG['user']}")
        
    
        cnx = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            port=DB_CONFIG['port']
        )
        cursor = cnx.cursor()
        
        print("Подключение успешно!")
        create_database(cursor)
        cnx.database = DB_NAME
        create_tables(cursor)
        insert_test_data(cursor)
        cnx.commit()
        print("База данных и тестовые данные созданы успешно!")
        
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Ошибка: Неверное имя пользователя или пароль")
            print("Проверьте настройки в файле db_config.py")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Ошибка: База данных не существует")
        else:
            print(f"Ошибка MySQL: {err}")
    except Exception as e:
        print(f"Общая ошибка: {e}")
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()
        print("Соединение закрыто.")

if __name__ == "__main__":
    main()
