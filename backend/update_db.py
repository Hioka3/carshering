import mysql.connector
from db_config import DB_CONFIG, DB_NAME

def update_database():
    cnx = None
    cursor = None
    try:
        print("Подключение к MySQL...")
        config = DB_CONFIG.copy()
        config['database'] = DB_NAME
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        
        print("Отключение проверки внешних ключей...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        print("Удаление связанных заказов...")
        cursor.execute("DELETE FROM orders")
        
        print("Удаление старой таблицы cars...")
        cursor.execute("DROP TABLE IF EXISTS cars")
        
        print("Включение проверки внешних ключей...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        print("Создание новой таблицы cars...")
        cursor.execute("""
            CREATE TABLE cars (
                id INT AUTO_INCREMENT PRIMARY KEY,
                model VARCHAR(100) NOT NULL,
                number VARCHAR(20) NOT NULL UNIQUE,
                status ENUM('available','booked','maintenance') DEFAULT 'available',
                price_per_hour DECIMAL(6,2) NOT NULL,
                image_url VARCHAR(500)
            ) ENGINE=InnoDB
        """)
        
        print("Добавление новых данных...")
        cars = [
            ("Tesla Model 3", "A111AA", 15.00, "https://images.unsplash.com/photo-1617788138017-80ad40651399?w=400"),
            ("BMW i3", "B222BB", 12.50, "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=400"),
            ("Kia Rio", "C333CC", 8.00, "https://images.unsplash.com/photo-1502877338535-766e1452684a?w=400"),
            ("Mercedes C-Class", "D444DD", 18.00, "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=400"),
            ("Toyota Camry", "E555EE", 10.00, "https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?w=400")
        ]
        
        for car in cars:
            cursor.execute("INSERT INTO cars (model, number, price_per_hour, image_url) VALUES (%s, %s, %s, %s)", car)
        
        cnx.commit()
        print("База данных успешно обновлена!")
        
    except mysql.connector.Error as err:
        print(f"Ошибка MySQL: {err}")
    except Exception as e:
        print(f"Общая ошибка: {e}")
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

if __name__ == "__main__":
    update_database()