from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime
from flask_cors import CORS
from db_config import DB_CONFIG, DB_NAME

app = Flask(__name__)
CORS(app)

def get_db():
    config = DB_CONFIG.copy()
    config['database'] = DB_NAME
    return mysql.connector.connect(**config)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    cnx = get_db()
    cursor = cnx.cursor(dictionary=True)
    try:
        cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                       (data['username'], data['password'], data['email']))
        cnx.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    finally:
        cursor.close()
        cnx.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    cnx = get_db()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (data['username'], data['password']))
    user = cursor.fetchone()
    cursor.close()
    cnx.close()
    if user:
        return jsonify({'success': True, 'user': user})
    else:
        return jsonify({'success': False})

@app.route('/api/cars')
def cars():
    cnx = get_db()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cars")
    cars = cursor.fetchall()
    cursor.close()
    cnx.close()
    return jsonify({'cars': cars})

@app.route('/api/book', methods=['POST'])
def book():
    data = request.json
    cnx = get_db()
    cursor = cnx.cursor(dictionary=True)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        cursor.execute("INSERT INTO orders (user_id, car_id, start_time, status) VALUES (%s, %s, %s, 'active')",
                       (data['user_id'], data['car_id'], now))
        cursor.execute("UPDATE cars SET status='booked' WHERE id=%s", (data['car_id'],))
        cnx.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    finally:
        cursor.close()
        cnx.close()

@app.route('/api/orders')
def orders():
    user_id = request.args.get('user_id')
    cnx = get_db()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("""
        SELECT o.*, c.model FROM orders o
        JOIN cars c ON o.car_id = c.id
        WHERE o.user_id=%s
        ORDER BY o.start_time DESC
    """, (user_id,))
    orders = cursor.fetchall()
    cursor.close()
    cnx.close()
    return jsonify({'orders': orders})

if __name__ == '__main__':
    app.run(debug=True)
