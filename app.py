import os
import json
import sqlite3
from flask import Flask, render_template, send_from_directory, request, jsonify

app = Flask(__name__)
DATA_FOLDER = 'data'      # Папка в корне для графики
DB_FILE = 'leads.db'      # Файл базы данных

# Загружаем JSON с текстами
def load_content():
    try:
        with open('content.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка чтения JSON: {e}")
        return {}

# Создаем БД, если нет
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS leads 
                        (id INTEGER PRIMARY KEY, name TEXT, email TEXT, phone TEXT, 
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
init_db()

# --- ROUTES ---

@app.route('/')
def index():
    return render_template('index.html', c=load_content())

# Магия: раздаем файлы из корневой папки data
@app.route('/data/<path:filename>')
def serve_data(filename):
    return send_from_directory(DATA_FOLDER, filename)

# Прием заявок
@app.route('/api/lead', methods=['POST'])
def add_lead():
    d = request.json
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO leads (name, email, phone) VALUES (?,?,?)",
                        (d.get('name'), d.get('email'), d.get('phone')))
            lid = cur.lastrowid
        # Эмуляция ссылки на оплату
        return jsonify({'status': 'ok', 'redirect': f'/pay?id={lid}'})
    except Exception as e:
        return jsonify({'status': 'error', 'msg': str(e)}), 500

@app.route('/pay')
def pay_mock():
    return "<body style='background:#050510;color:#00F0FF;height:100vh;display:flex;align-items:center;justify-content:center'><h1>💳 ШЛЮЗ ОПЛАТЫ (ТЕСТ)</h1></body>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
