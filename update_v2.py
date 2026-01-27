import os

# === 1. ОБНОВЛЕННЫЙ CSS (Фикс видео и стили игры) ===
css_code = """:root { --bg: #050510; --neon: #00F0FF; --err: #FF2050; --gold: #FFAA00; --font-h: 'Unbounded', sans-serif; --font-c: 'JetBrains Mono', monospace; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: var(--bg); color: #fff; font-family: 'Inter', sans-serif; overflow-x: hidden; }

/* HERO VIDEO FIX */
.hero { 
    position: relative; 
    height: 100vh; 
    display: flex; 
    align-items: center; 
    justify-content: center; 
    overflow: hidden; 
    background: #000;
}
.video-wrap { 
    position: absolute; 
    top: 0; left: 0; 
    width: 100%; height: 100%; 
    z-index: 0; 
}
.hero-bg { 
    width: 100%; height: 100%; 
    object-fit: cover; 
    opacity: 0.6; 
}
.hero-overlay {
    position: absolute; inset: 0;
    background: radial-gradient(circle, rgba(5,5,16,0.2) 0%, rgba(5,5,16,0.9) 100%);
    z-index: 1;
}
.hero-content { 
    position: relative; z-index: 2; 
    text-align: center; padding: 20px; 
    max-width: 900px; 
}

/* СТИЛИ ИГРЫ */
.cards { display: flex; gap: 20px; flex-wrap: wrap; justify-content: center; width: 100%; }
.card { 
    width: 300px; height: 500px; 
    border: 2px solid #333; 
    position: relative; 
    cursor: pointer; 
    background: #000; 
    overflow: hidden; 
    transition: 0.3s; 
}
.card video { width: 100%; height: 100%; object-fit: cover; display: block; }
.card:hover { border-color: var(--neon); transform: translateY(-5px); }

/* Состояние Ошибки */
.card.disabled { pointer-events: none; border-color: var(--err); transform: none; }
.err-msg {
    height: 100%; display: flex; flex-direction: column; 
    align-items: center; justify-content: center; 
    background: rgba(20,0,0,0.9); color: var(--err); 
    text-align: center; padding: 10px;
}

/* Форма Победителя */
.win-box { 
    background: rgba(0, 240, 255, 0.05); 
    border: 2px solid var(--neon); 
    padding: 40px; border-radius: 12px; 
    text-align: center; max-width: 500px; 
    margin: 0 auto; animation: popIn 0.5s; 
}
.win-box input { 
    width: 100%; padding: 12px; margin-bottom: 10px; 
    background: #000; border: 1px solid #333; color: #fff; 
}

/* ОСТАЛЬНОЕ */
.btn-neon { background: var(--neon); color: #000; border: none; padding: 15px 40px; font-family: var(--font-h); font-weight: 800; cursor: pointer; clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), 0 100%, 0 10px); transition: 0.3s; width: 100%; text-transform: uppercase; }
.btn-neon:hover { transform: scale(1.05); box-shadow: 0 0 20px var(--neon); }
.title { font-family: var(--font-h); font-size: 2.5rem; text-align: center; margin-bottom: 40px; }
.section { padding: 80px 20px; min-height: 80vh; display: flex; flex-direction: column; justify-content: center; position: relative; z-index: 2; }
.glitch { font-size: clamp(40px, 6vw, 100px); font-family: var(--font-h); line-height: 1; margin-bottom: 20px; }
.subtitle { color: var(--neon); font-family: var(--font-c); letter-spacing: 2px; }
.sys-msg { background: rgba(0,0,0,0.8); border-left: 3px solid var(--neon); padding: 20px; margin: 30px auto; text-align: left; font-family: var(--font-c); }
.hl { color: var(--neon); display: block; margin-top: 5px; }
.stats-row { display: flex; justify-content: center; gap: 40px; flex-wrap: wrap; text-align: center; }
.val { font-size: 3rem; color: var(--neon); font-family: var(--font-h); }
.iron-man { height: 300vh; position: relative; background: #000; }
.sticky-wrap { position: sticky; top: 0; height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; overflow: hidden; }
.layers { position: relative; width: 400px; height: 700px; }
.layer { position: absolute; inset: 0; opacity: 0; transition: opacity 0.5s; display: flex; flex-direction: column; align-items: center; }
.layer img { width: 100%; height: 100%; object-fit: contain; }
.caption { position: absolute; bottom: 50px; background: rgba(0,0,0,0.9); padding: 15px; border: 1px solid #333; text-align: center; width: 100%; }
.term-box, .gen-box, .offer-card { background: #0d1117; border: 1px solid #333; padding: 20px; border-radius: 10px; width: 100%; max-width: 600px; margin: 0 auto; }
.term-body { height: 250px; overflow-y: auto; font-family: var(--font-c); color: #ccc; margin: 15px 0; }
.usr { color: var(--neon); }
input, select, textarea { width: 100%; background: #000; border: 1px solid #333; color: #fff; padding: 15px; margin-bottom: 15px; outline: none; }
.price { font-size: 3rem; font-family: var(--font-h); margin: 20px 0; }
.old { text-decoration: line-through; color: #666; font-size: 1.5rem; margin-right: 15px; }
.alert { color: var(--err); font-family: var(--font-c); margin-bottom: 20px; }
#matrix { position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.15; }
@keyframes popIn { from {transform:scale(0.9); opacity:0} to {transform:scale(1); opacity:1} }
"""

# === 2. ОБНОВЛЕННЫЙ HTML (Новая структура Hero и Игры) ===
html_code = """<!DOCTYPE html>
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
        <div class="video-wrap">
            <video autoplay muted loop playsinline class="hero-bg">
                <source src="/data/{{ c.hero.media }}" type="video/mp4">
            </video>
            <div class="hero-overlay"></div>
        </div>
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
        <div class="timer" style="text-align:center; font-family:'JetBrains Mono'; margin-bottom:20px; color:#FF2050">
            ВРЕМЯ: <span id="g-timer">{{ c.game.timer_sec }}</span>
        </div>
        
        <div id="game-area" class="cards">
            {% for card in c.game.cards %}
            <div class="card" onclick="handleCard(this, {{ 'true' if card.is_real else 'false' }})">
                <video src="/data/{{ card.file }}" loop muted onmouseover="this.play()" onmouseout="this.pause()"></video>
            </div>
            {% endfor %}
        </div>
    </section>

    <section class="section"><h2 class="title">{{ c.stats.title }}</h2><div class="stats-row">{% for item in c.stats.stat_list %}<div class="stat"><div class="val">{{ item.val }}</div><div class="desc">{{ item.text }}</div></div>{% endfor %}</div></section>
    <section class="iron-man"><div class="sticky-wrap"><div class="layers">{% for layer in c.iron.layers %}<div class="layer layer-{{ loop.index }}"><img src="/data/{{ layer.file }}"><div class="caption"><h3>{{ layer.title }}</h3><p>{{ layer.desc }}</p></div></div>{% endfor %}</div><div class="scroll-hint">{{ c.iron.scroll_hint }}</div></div></section>
    <section class="section"><h2 class="title">{{ c.terminal.title }}</h2><div class="term-box"><div class="term-head"><span class="dot r" style="display:inline-block;width:10px;height:10px;background:red;border-radius:50%"></span> {{ c.terminal.head }}</div><div class="term-body" id="term-out"><div><span class="usr">user@unit:~$</span> ...</div></div><button class="btn-neon" style="width:100%;margin-top:10px" onclick="runTerm()">{{ c.terminal.btn }}</button></div></section>
    <section class="section"><h2 class="title">{{ c.gen.title }}</h2><div class="gen-box"><label>{{ c.gen.lbl_1 }}</label><input type="text" id="g-topic" placeholder="Python..."><label>{{ c.gen.lbl_2 }}</label><select id="g-lvl">{% for l in c.gen.levels %}<option>{{ l }}</option>{% endfor %}</select><button class="btn-neon" onclick="runGen()">{{ c.gen.btn }}</button><textarea id="g-res" readonly></textarea></div></section>
    
    <section class="section">
        <div class="offer-card">
            <h2 class="title">{{ c.offer.title }}</h2>
            <ul class="feats" style="text-align:left;list-style:none;line-height:2">{% for f in c.offer.feats %}<li>{{ f }}</li>{% endfor %}</ul>
            <div class="price"><span class="old">{{ c.offer.price_old }}</span> <span class="new" style="color:#00F0FF">{{ c.offer.price_new }}</span></div>
            <div class="alert">{{ c.offer.timer_lbl }} <span id="o-timer">15:00</span></div>
            <form onsubmit="sendLead(event, 'footer_offer')">
                <input type="text" name="name" placeholder="Имя" required>
                <input type="email" name="email" placeholder="Email" required>
                <input type="tel" name="phone" placeholder="Телефон" required>
                <button type="submit" class="btn-neon">{{ c.offer.form_btn }}</button>
            </form>
        </div>
    </section>

    <script>const LOGS = {{ c.terminal.logs | tojson }};</script>
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>"""

# === 3. ОБНОВЛЕННЫЙ JS (Логика: Попытки, Замена блоков) ===
js_code = """document.addEventListener('DOMContentLoaded', () => {
    
    // Matrix & Glitch
    const cvs = document.getElementById('matrix'); const ctx = cvs.getContext('2d');
    function resize(){cvs.width=window.innerWidth;cvs.height=window.innerHeight} window.onresize=resize; resize();
    setInterval(()=>{ctx.fillStyle='#0001';ctx.fillRect(0,0,cvs.width,cvs.height);ctx.fillStyle='#0F0';
    for(let i=0;i<Math.floor(cvs.width/20);i++)if(Math.random()>0.975)ctx.fillText(String.fromCharCode(Math.random()*128),i*20,Math.random()*cvs.height)},50);
    const t=document.querySelector('.glitch'); if(t){const txt=t.getAttribute('data-text');let i=0;
    const inv=setInterval(()=>{t.innerText=txt.split("").map((l,x)=>x<i?txt[x]:"X0#@"[Math.floor(Math.random()*4)]).join("");if(i>=txt.length)clearInterval(inv);i+=1/3},40)}

    // --- GAME LOGIC ---
    let gameActive = true;
    let attempts = 0;
    let timer = 60;
    setInterval(() => { if(timer>0 && gameActive) document.getElementById('g-timer').innerText = --timer; }, 1000);

    window.handleCard = (el, isReal) => {
        if(!gameActive || el.classList.contains('disabled')) return;
        attempts++;

        if(!isReal) {
            // ОШИБКА: Заменяем видео на текст
            el.classList.add('disabled');
            el.innerHTML = `
                <div class="err-msg">
                    <div style="font-size:3rem;">❌</div>
                    <div style="font-family:'Unbounded';margin-top:10px">ОШИБКА</div>
                    <div style="font-size:0.8rem; opacity:0.7">Это ИИ-клон</div>
                </div>
            `;
        } else {
            // ПОБЕДА
            gameActive = false;
            const area = document.getElementById('game-area');
            
            if(attempts === 1) {
                // С 1-й попытки -> ФОРМА ПОБЕДИТЕЛЯ
                area.innerHTML = `
                    <div class="win-box">
                        <h3 style="font-size:1.5rem">✅ ВЫ УГАДАЛИ С 1-Й ПОПЫТКИ!</h3>
                        <p style="color:#00F0FF;">Ваша интуиция работает. Заберите скидку 50%.</p>
                        <form onsubmit="sendLead(event, 'game_winner_50')">
                            <input type="text" name="name" placeholder="Имя" required>
                            <input type="tel" name="phone" placeholder="Телефон" required>
                            <input type="email" name="email" placeholder="Email для промокода" required>
                            <button type="submit" class="btn-neon">ЗАБРАТЬ ПРОМОКОД</button>
                        </form>
                    </div>`;
            } else {
                // Не с 1-й попытки -> Сообщение
                area.innerHTML = `
                    <div class="win-box" style="border-color:#FFAA00">
                        <h3 style="color:#FFAA00">ВЫ НАШЛИ ЧЕЛОВЕКА</h3>
                        <p>Но понадобилось ${attempts} попытки.</p>
                        <p>Промокод на 50% сгорел, но вы все еще можете получить скидку 90% в конце сайта.</p>
                    </div>`;
            }
        }
    };

    // Общая функция отправки лида
    window.sendLead = async (e, source) => {
        e.preventDefault();
        const btn = e.target.querySelector('button');
        const old = btn.innerText;
        btn.innerText = "ОТПРАВКА...";
        
        const d = new FormData(e.target);
        const data = Object.fromEntries(d);
        data.source = source; // Добавляем метку

        try {
            const res = await fetch('/api/lead', {
                method:'POST', headers:{'Content-Type':'application/json'},
                body: JSON.stringify(data)
            });
            const j = await res.json();
            
            if(j.status === 'ok') {
                if(source === 'game_winner_50') {
                    // Показываем код
                    e.target.parentElement.innerHTML = `<h3>ЗАЯВКА ПРИНЯТА!</h3><p>Ваш промокод: <span style="color:#00F0FF;font-size:1.5rem">NEURO50</span></p>`;
                } else {
                    // Редирект
                    window.location.href = j.redirect;
                }
            } else { alert("Error"); btn.innerText = old; }
        } catch(err) { alert("Network Error"); btn.innerText = old; }
    };
    
    // Scroll & Term & Gen
    const iron = document.querySelector('.iron-man'); const layers = document.querySelectorAll('.layer');
    if(iron) { window.onscroll = () => {
        const r = iron.getBoundingClientRect(); const p = -r.top / (r.height - window.innerHeight);
        if(p>0 && p<1.2) { layers[0].style.opacity=1; layers[1].style.opacity=p>0.33?1:0; layers[2].style.opacity=p>0.66?1:0; }
    }};
    window.runTerm=()=>{const o=document.getElementById('term-out');let k=0;function l(){if(k<LOGS.length){o.innerHTML+=`<div>${LOGS[k]}</div>`;o.scrollTop=o.scrollHeight;k++;setTimeout(l,600)}}l()};
    window.runGen=()=>{const t=document.getElementById('g-topic').value;const l=document.getElementById('g-lvl').value;const r=document.getElementById('g-res');const x=`Role: Tutor ${t}. Level: ${l}.`;r.value="";let i=0;const n=setInterval(()=>{r.value+=x[i];i++;if(i>=x.length)clearInterval(n)},30)};
    window.scrollToId=(id)=>document.getElementById(id).scrollIntoView({behavior:'smooth'});
});
"""

# === 4. ОБНОВЛЕННЫЙ APP.PY (База с source) ===
app_code = """import os
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
    opener = urllib.request.build_opener(); opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
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
        conn.execute("CREATE TABLE IF NOT EXISTS leads (id INTEGER PRIMARY KEY, name TEXT, email TEXT, phone TEXT, source TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

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
            c.execute("INSERT INTO leads (name, email, phone, source) VALUES (?,?,?,?)", 
                      (d.get('name'), d.get('email'), d.get('phone'), d.get('source', 'unknown')))
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

with open('static/css/style.css', 'w', encoding='utf-8') as f: f.write(css_code)
with open('templates/index.html', 'w', encoding='utf-8') as f: f.write(html_code)
with open('static/js/main.js', 'w', encoding='utf-8') as f: f.write(js_code)
with open('app.py', 'w', encoding='utf-8') as f: f.write(app_code)

print("✅ ФАЙЛЫ ОБНОВЛЕНЫ. ЗАПУСКАЙТЕ СЕРВЕР.")
