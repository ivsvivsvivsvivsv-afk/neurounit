import os
import json
import sqlite3
import urllib.request
from flask import Flask, render_template, send_from_directory, request, jsonify

app = Flask(__name__)

# --- НАСТРОЙКИ ПУТЕЙ ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, 'data')
CONTENT_FILE = os.path.join(BASE_DIR, 'content.json')
DB_FILE = os.path.join(BASE_DIR, 'leads.db')

# --- ФУНКЦИЯ АВТО-НАСТРОЙКИ (Скачивание заглушек) ---
def setup_dummy_content():
    # Ссылки на временные файлы
    DUMMY_VIDEO = "https://assets.mixkit.co/videos/preview/mixkit-digital-animation-of-blue-connections-9060-large.mp4"
    DUMMY_IMG = "https://placehold.co/600x800/050510/00F0FF.png?text=LOADING..."
    
    # 1. Создаем папку data
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
        print(f"📁 Папка {DATA_FOLDER} создана.")

    # 2. Настраиваем 'качальщик' (притворяемся браузером, чтобы Mixkit не банил)
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')]
    urllib.request.install_opener(opener)

    try:
        # Проверяем наличие content.json
        if not os.path.exists(CONTENT_FILE):
            print("❌ ОШИБКА: Файл content.json не найден! Создайте его вручную.")
            return

        with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        print("⏳ Проверка файлов контента...")
        
        # Функция безопасного скачивания
        def check_and_download(filename, url):
            if not filename: return
            filepath = os.path.join(DATA_FOLDER, filename)
            if not os.path.exists(filepath):
                print(f"⬇️ Скачиваю заглушку: {filename}")
                try:
                    urllib.request.urlretrieve(url, filepath)
                except Exception as e:
                    print(f"⚠️ Не удалось скачать {filename}: {e}")

        # Проходим по JSON и качаем всё, чего нет
        if 'hero' in data: check_and_download(data['hero'].get('media'), DUMMY_VIDEO)
        if 'game' in data:
            for card in data['game'].get('cards', []): check_and_download(card.get('file'), DUMMY_VIDEO)
        if 'iron' in data:
            for layer in data['iron'].get('layers', []): check_and_download(layer.get('file'), DUMMY_IMG)
            
        print("✅ Все файлы готовы к запуску.")
        
    except Exception as e:
        print(f"⚠️ Ошибка при проверке контента: {e}")

# --- БАЗА ДАННЫХ ---
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS leads 
                        (id INTEGER PRIMARY KEY, name TEXT, email TEXT, phone TEXT, 
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

# --- СЕРВЕР ---
@app.route('/')
def index():
    try:
        with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
            content = json.load(f)
    except:
        content = {} # Чтобы сайт не упал, если json сломан
    return render_template('index.html', c=content)

@app.route('/data/<path:filename>')
def serve_data(filename):
    return send_from_directory(DATA_FOLDER, filename)

@app.route('/api/lead', methods=['POST'])
def add_lead():
    d = request.json
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO leads (name, email, phone) VALUES (?,?,?)",
                        (d.get('name'), d.get('email'), d.get('phone')))
            lid = cur.lastrowid
        return jsonify({'status': 'ok', 'redirect': f'/pay?id={lid}'})
    except Exception as e:
        return jsonify({'status': 'error', 'msg': str(e)}), 500

@app.route('/pay')
def pay_mock():
    return "<body style='background:#050510;color:#00F0FF;height:100vh;display:flex;align-items:center;justify-content:center;font-family:monospace'><h1>💳 ШЛЮЗ ОПЛАТЫ (ТЕСТ)</h1></body>"

if __name__ == '__main__':
    # Сначала проверяем базу и файлы, потом запускаем сайт
    init_db()
    setup_dummy_content()
    print("\n🚀 ЗАПУСК СЕРВЕРА...")
    app.run(host='0.0.0.0', port=5000)
