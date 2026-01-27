import os

# 1. ИСПРАВЛЕННЫЙ CONTENT.JSON (items -> stat_list)
content_json = """{
  "meta": {
    "title": "НЕЙРО-ЮНИТ | Трансформация"
  },
  "hero": {
    "title": "НЕЙРО-ЮНИТ",
    "subtitle": "НОВАЯ ЭРА ОБРАЗОВАНИЯ АКТИВИРОВАНА",
    "msg_1": "[СИСТЕМНОЕ СООБЩЕНИЕ]: Оставайтесь до конца.",
    "msg_2": "Первые 10 участников получат скидку 90%.",
    "btn": "АКТИВИРОВАТЬ СИСТЕМУ",
    "media": "hero_bg.mp4"
  },
  "game": {
    "title": "ТЕСТ ТЬЮРИНГА",
    "timer_sec": 60,
    "success_msg": "ДОСТУП РАЗРЕШЕН",
    "fail_msg": "ОШИБКА: ОБНАРУЖЕН ИИ",
    "alert_success": "СИСТЕМА: Человек подтвержден. Скидка зафиксирована.",
    "cards": [
      { "file": "video_fake_1.mp4", "is_real": false },
      { "file": "video_real.mp4", "is_real": true },
      { "file": "video_fake_2.mp4", "is_real": false }
    ]
  },
  "stats": {
    "title": "МИР ИЗМЕНИЛСЯ",
    "stat_list": [
      { "val": "100M", "text": "Пользователей ChatGPT за 2 месяца" },
      { "val": "85M", "text": "Рабочих мест исчезнет к 2025" },
      { "val": "300M", "text": "Под угрозой (Goldman Sachs)" }
    ]
  },
  "iron": {
    "scroll_hint": "ЛИСТАЙ ВНИЗ ↓",
    "layers": [
      {
        "title": "УРОВЕНЬ 1: ТЫ",
        "desc": "Твой мозг, опыт и амбиции.",
        "file": "layer_1.png"
      },
      {
        "title": "УРОВЕНЬ 2: НЕЙРОСКЕЛЕТ",
        "desc": "ChatGPT, Perplexity, Veo3.",
        "file": "layer_2.png"
      },
      {
        "title": "УРОВЕНЬ 3: НЕЙРО-ЮНИТ",
        "desc": "Суперсила: Критическое мышление + ИИ.",
        "file": "layer_3.png"
      }
    ]
  },
  "terminal": {
    "title": "СБОР ДАННЫХ",
    "head": "perplexity_pro.exe",
    "btn": "[ ЗАПУСТИТЬ ПОИСК: GOOGLE VEO3 ]",
    "logs": [
      "> Connecting to Neural Network...",
      "> Searching: 'Google Veo3 specs'...",
      "> Scanning 14,200 sources...",
      "> Filtering hallucinations...",
      "<br><span style='color:#fff'>RESULT:</span> Google Veo3 — GenAI Video Model.",
      "Status: Beta. Resolution: 1080p.",
      "<span style='background:#00F0FF; color:black'>[DATASET COMPILED IN 1.2S]</span>"
    ]
  },
  "gen": {
    "title": "КОНСТРУКТОР ПЕДАГОГА",
    "lbl_1": "ТЕМА",
    "lbl_2": "УРОВЕНЬ",
    "btn": "СГЕНЕРИРОВАТЬ ПРОМТ",
    "levels": ["Новичок", "Средний", "Профи"]
  },
  "offer": {
    "title": "НЕЙРОСКЕЛЕТ",
    "feats": [
      "✅ 10 ИИ-педагогов",
      "✅ База знаний NotebookLM",
      "✅ Продвинутый фактчекинг",
      "🎁 Бонус: Модуль Veo3 Mastery"
    ],
    "price_old": "29,990 ₽",
    "price_new": "2,990 ₽",
    "timer_lbl": "ПРЕДЛОЖЕНИЕ ИСЧЕЗНЕТ ЧЕРЕЗ:",
    "form_btn": "ТРАНСФОРМИРОВАТЬСЯ"
  }
}"""

# 2. ИСПРАВЛЕННЫЙ HTML (c.stats.items -> c.stats.stat_list)
index_html = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ c.meta.title }}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=JetBrains+Mono:wght@400;700&family=Unbounded:wght@400;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <canvas id="matrix"></canvas>

    <section class="hero">
        <video autoplay muted loop playsinline class="hero-bg">
            <source src="/data/{{ c.hero.media }}" type="video/mp4">
        </video>
        <div class="overlay"></div>
        <div class="hero-content">
            <h1 class="glitch" data-text="{{ c.hero.title }}">{{ c.hero.title }}</h1>
            <p class="subtitle">> {{ c.hero.subtitle }}</p>
            <div class="sys-msg">
                <span>{{ c.hero.msg_1 }}</span>
                <span class="hl">{{ c.hero.msg_2 }}</span>
            </div>
            <button class="btn-neon" onclick="scrollToId('game')">{{ c.hero.btn }}</button>
        </div>
    </section>

    <section id="game" class="section">
        <h2 class="title">{{ c.game.title }}</h2>
        <div class="timer">00:<span id="g-timer">{{ c.game.timer_sec }}</span></div>
        <div class="cards">
            {% for card in c.game.cards %}
            <div class="card" onclick="checkClone(this, {{ 'true' if card.is_real else 'false' }})">
                <div class="status err">{{ c.game.fail_msg }}</div>
                <div class="status succ">{{ c.game.success_msg }}</div>
                <video src="/data/{{ card.file }}" loop muted onmouseover="this.play()" onmouseout="this.pause()"></video>
            </div>
            {% endfor %}
        </div>
    </section>

    <section class="section">
        <h2 class="title">{{ c.stats.title }}</h2>
        <div class="stats-row">
            {% for item in c.stats.stat_list %}
            <div class="stat">
                <div class="val">{{ item.val }}</div>
                <div class="desc">{{ item.text }}</div>
            </div>
            {% endfor %}
        </div>
    </section>

    <section class="iron-man">
        <div class="sticky-wrap">
            <div class="layers">
                {% for layer in c.iron.layers %}
                <div class="layer layer-{{ loop.index }}">
                    <img src="/data/{{ layer.file }}" alt="Layer">
                    <div class="caption">
                        <h3>{{ layer.title }}</h3>
                        <p>{{ layer.desc }}</p>
                    </div>
                </div>
                {% endfor %}
            </div>
            <div class="scroll-hint">{{ c.iron.scroll_hint }}</div>
        </div>
    </section>

    <section class="section">
        <h2 class="title">{{ c.terminal.title }}</h2>
        <div class="term-box">
            <div class="term-head">
                <span class="dot r"></span><span class="dot y"></span><span class="dot g"></span> {{ c.terminal.head }}
            </div>
            <div class="term-body" id="term-out">
                <div><span class="usr">user@unit:~$</span> ...</div>
            </div>
            <button class="btn-sec" onclick="runTerm()">{{ c.terminal.btn }}</button>
        </div>
    </section>

    <section class="section">
        <h2 class="title">{{ c.gen.title }}</h2>
        <div class="gen-box">
            <label>{{ c.gen.lbl_1 }}</label>
            <input type="text" id="g-topic" placeholder="Python...">
            <label>{{ c.gen.lbl_2 }}</label>
            <select id="g-lvl">{% for l in c.gen.levels %}<option>{{ l }}</option>{% endfor %}</select>
            <button class="btn-neon" onclick="runGen()">{{ c.gen.btn }}</button>
            <textarea id="g-res" readonly></textarea>
        </div>
    </section>

    <section class="section">
        <div class="offer-card">
            <h2 class="title neon">{{ c.offer.title }}</h2>
            <ul class="feats">{% for f in c.offer.feats %}<li>{{ f }}</li>{% endfor %}</ul>
            <div class="price">
                <span class="old">{{ c.offer.price_old }}</span>
                <span class="new">{{ c.offer.price_new }}</span>
            </div>
            <div class="alert">{{ c.offer.timer_lbl }} <span id="o-timer">15:00</span></div>
            <form id="lead-form">
                <input type="text" name="name" placeholder="Имя" required>
                <input type="email" name="email" placeholder="Email" required>
                <input type="tel" name="phone" placeholder="Телефон" required>
                <button type="submit" class="btn-neon">{{ c.offer.form_btn }}</button>
            </form>
        </div>
    </section>

    <script>
        const LOGS = {{ c.terminal.logs | tojson }};
        const GAME_ALERT = "{{ c.game.alert_success }}";
    </script>
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>"""

# 3. ИСПРАВЛЕННЫЙ APP.PY (С автозагрузкой заглушек)
app_py = """import os
import json
import sqlite3
import urllib.request
from flask import Flask, render_template, send_from_directory, request, jsonify

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, 'data')
CONTENT_FILE = os.path.join(BASE_DIR, 'content.json')
DB_FILE = os.path.join(BASE_DIR, 'leads.db')

def setup_dummy_content():
    if not os.path.exists(DATA_FOLDER): os.makedirs(DATA_FOLDER)
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    
    if not os.path.exists(CONTENT_FILE): return

    try:
        with open(CONTENT_FILE, 'r', encoding='utf-8') as f: data = json.load(f)
        
        def dl(name, url):
            if not name: return
            p = os.path.join(DATA_FOLDER, name)
            if not os.path.exists(p):
                try: urllib.request.urlretrieve(url, p)
                except: pass

        VID = "https://assets.mixkit.co/videos/preview/mixkit-digital-animation-of-blue-connections-9060-large.mp4"
        IMG = "https://placehold.co/600x800/050510/00F0FF.png?text=LOADING..."

        if 'hero' in data: dl(data['hero'].get('media'), VID)
        if 'game' in data:
            for c in data['game'].get('cards', []): dl(c.get('file'), VID)
        if 'iron' in data:
            for l in data['iron'].get('layers', []): dl(l.get('file'), IMG)
            
    except: pass

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS leads (id INTEGER PRIMARY KEY, name TEXT, email TEXT, phone TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

@app.route('/')
def index():
    try:
        with open(CONTENT_FILE, 'r', encoding='utf-8') as f: content = json.load(f)
    except: content = {}
    return render_template('index.html', c=content)

@app.route('/data/<path:filename>')
def serve_data(filename): return send_from_directory(DATA_FOLDER, filename)

@app.route('/api/lead', methods=['POST'])
def add_lead():
    d = request.json
    try:
        with sqlite3.connect(DB_FILE) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO leads (name, email, phone) VALUES (?,?,?)", (d.get('name'), d.get('email'), d.get('phone')))
            lid = c.lastrowid
        return jsonify({'status': 'ok', 'redirect': f'/pay?id={lid}'})
    except Exception as e: return jsonify({'status': 'error', 'msg': str(e)}), 500

@app.route('/pay')
def pay(): return "<body style='background:#050510;color:#00F0FF;display:flex;justify-content:center;align-items:center;height:100vh;font-family:monospace'><h1>ПЛАТЕЖНЫЙ ШЛЮЗ</h1></body>"

if __name__ == '__main__':
    init_db()
    setup_dummy_content()
    app.run(host='0.0.0.0', port=5000)
"""

# ЗАПИСЬ ФАЙЛОВ
with open('content.json', 'w', encoding='utf-8') as f: f.write(content_json)
print("✅ content.json исправлен")

if not os.path.exists('templates'): os.makedirs('templates')
with open('templates/index.html', 'w', encoding='utf-8') as f: f.write(index_html)
print("✅ templates/index.html исправлен")

with open('app.py', 'w', encoding='utf-8') as f: f.write(app_py)
print("✅ app.py обновлен")

print("\n🚀 ВСЕ ГОТОВО! ЗАПУСКАЙТЕ КОМАНДУ: python app.py")
