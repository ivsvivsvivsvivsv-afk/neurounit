#!/usr/bin/env python3
"""
НЕЙРО-ЮНИТ: Скрипт обновления v3
================================

Решает проблемы:
1. Видео hero_bg.mp4 не проигрывается → добавлен fallback + poster
2. Матрица пропала → восстановлена полноценная анимация
3. Блок СБОР ДАННЫХ → теперь выводит качественный промт для Perplexity по VEO3
4. Конструктор педагога → генерирует полный промт с подстановкой темы и уровня

Запуск: python update_v3.py
"""

import os

# ================================================
# 1. CSS - Полный стиль с фиксом видео и матрицей
# ================================================
CSS_CODE = r''':root { 
    --bg: #050510; 
    --neon: #00F0FF; 
    --err: #FF2050; 
    --gold: #FFAA00; 
    --font-h: 'Unbounded', sans-serif; 
    --font-c: 'JetBrains Mono', monospace; 
}

* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: var(--bg); color: #fff; font-family: 'Inter', sans-serif; overflow-x: hidden; }

/* MATRIX CANVAS */
#matrix { 
    position: fixed; 
    top: 0; left: 0; 
    width: 100%; height: 100%;
    z-index: 0; 
    opacity: 0.12;
    pointer-events: none;
}

/* HERO SECTION */
.hero { 
    position: relative; 
    height: 100vh; 
    display: flex; 
    align-items: center; 
    justify-content: center; 
    overflow: hidden; 
    background: #000;
    z-index: 10;
}

.video-wrap { 
    position: absolute; 
    top: 0; left: 0; 
    width: 100%; height: 100%; 
    z-index: 0; 
    background: #000;
}

.hero-bg { 
    width: 100%; 
    height: 100%; 
    object-fit: cover; 
    opacity: 0.6;
    display: block;
}

.hero-bg-animated {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: linear-gradient(135deg, #050510 0%, #0a1a2e 25%, #051525 50%, #0a1a2e 75%, #050510 100%);
    background-size: 400% 400%;
    animation: bgPulse 15s ease infinite;
    z-index: -2;
}

@keyframes bgPulse {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

.hero-overlay {
    position: absolute; inset: 0;
    background: radial-gradient(circle at center, rgba(5,5,16,0.2) 0%, rgba(5,5,16,0.95) 100%);
    z-index: 1;
}

.hero-content { 
    position: relative; z-index: 2; 
    text-align: center; padding: 20px; 
    max-width: 900px; 
}

/* TYPOGRAPHY */
.glitch { 
    font-size: clamp(40px, 8vw, 100px); 
    font-family: var(--font-h); 
    line-height: 1; 
    margin-bottom: 20px;
    text-shadow: 0 0 20px rgba(0,240,255,0.5);
}

.subtitle { 
    color: var(--neon); 
    font-family: var(--font-c); 
    letter-spacing: 2px;
    font-size: clamp(14px, 2vw, 18px);
}

.sys-msg { 
    background: rgba(0,0,0,0.8); 
    border-left: 3px solid var(--neon); 
    padding: 20px; 
    margin: 30px auto; 
    text-align: left; 
    font-family: var(--font-c);
    max-width: 600px;
}

.hl { color: var(--neon); display: block; margin-top: 5px; }

/* BUTTONS */
.btn-neon { 
    background: var(--neon); 
    color: #000; 
    border: none; 
    padding: 15px 40px; 
    font-family: var(--font-h); 
    font-weight: 800; 
    cursor: pointer; 
    clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px); 
    transition: 0.3s;
    text-transform: uppercase;
    font-size: 14px;
}

.btn-neon:hover { 
    transform: scale(1.05); 
    box-shadow: 0 0 30px var(--neon); 
}

.btn-neon:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
}

/* SECTIONS */
.title { 
    font-family: var(--font-h); 
    font-size: clamp(1.8rem, 4vw, 2.5rem); 
    text-align: center; 
    margin-bottom: 40px;
}

.section { 
    padding: 80px 20px; 
    min-height: 80vh; 
    display: flex; 
    flex-direction: column; 
    justify-content: center;
    align-items: center;
    position: relative; 
    z-index: 2;
}

/* GAME */
.timer {
    text-align: center;
    font-family: var(--font-c);
    font-size: 2rem;
    margin-bottom: 30px;
    color: var(--err);
}

.cards { 
    display: flex; 
    gap: 20px; 
    flex-wrap: wrap; 
    justify-content: center; 
    max-width: 1000px;
}

.card { 
    width: 280px; height: 450px; 
    border: 2px solid #333; 
    position: relative; 
    cursor: pointer; 
    background: #000; 
    overflow: hidden; 
    transition: 0.3s;
    border-radius: 8px;
}

.card video { width: 100%; height: 100%; object-fit: cover; display: block; }
.card:hover { border-color: var(--neon); transform: translateY(-5px); box-shadow: 0 10px 30px rgba(0,240,255,0.2); }
.card.disabled { pointer-events: none; border-color: var(--err); transform: none; }

.err-msg {
    height: 100%; display: flex; flex-direction: column; 
    align-items: center; justify-content: center; 
    background: rgba(20,0,0,0.95); color: var(--err); 
    text-align: center; padding: 20px;
}

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

@keyframes popIn { from {transform:scale(0.9); opacity:0} to {transform:scale(1); opacity:1} }

/* STATS */
.stats-row { display: flex; justify-content: center; gap: 40px; flex-wrap: wrap; text-align: center; }
.stat { padding: 20px; }
.val { font-size: clamp(2rem, 5vw, 3.5rem); color: var(--neon); font-family: var(--font-h); }
.desc { color: #aaa; max-width: 200px; }

/* IRON MAN */
.iron-man { height: 300vh; position: relative; }
.sticky-wrap { position: sticky; top: 0; height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; overflow: hidden; }
.layers { position: relative; width: 350px; height: 600px; }
.layer { position: absolute; inset: 0; opacity: 0; transition: opacity 0.6s ease; display: flex; flex-direction: column; align-items: center; }
.layer img { width: 100%; height: 100%; object-fit: contain; }
.caption { position: absolute; bottom: 30px; background: rgba(0,0,0,0.95); padding: 20px; border: 1px solid #333; text-align: center; width: 100%; border-radius: 8px; }
.caption h3 { color: var(--neon); font-family: var(--font-h); margin-bottom: 10px; }
.scroll-hint { position: absolute; bottom: 30px; color: var(--neon); font-family: var(--font-c); animation: bounce 2s infinite; }
@keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(10px); } }

/* TERMINAL */
.term-box { 
    background: #0d1117; border: 1px solid #333; 
    padding: 0; border-radius: 10px; 
    width: 100%; max-width: 700px; margin: 0 auto;
    overflow: hidden;
}

.term-head {
    background: #161b22;
    padding: 12px 15px;
    display: flex;
    align-items: center;
    gap: 8px;
    border-bottom: 1px solid #333;
}

.dot { width: 12px; height: 12px; border-radius: 50%; display: inline-block; }
.dot.r { background: #ff5f56; }
.dot.y { background: #ffbd2e; }
.dot.g { background: #27ca40; }

.term-body { 
    height: 300px; overflow-y: auto; 
    font-family: var(--font-c); color: #8b949e; 
    padding: 20px; font-size: 14px; line-height: 1.6;
}

.usr { color: var(--neon); }
.success { color: #27ca40; }

.term-footer { padding: 15px; border-top: 1px solid #333; }

/* GENERATOR */
.gen-box { 
    background: #0d1117; border: 1px solid #333; 
    padding: 30px; border-radius: 10px; 
    width: 100%; max-width: 800px; margin: 0 auto;
}

.gen-box label {
    display: block; color: var(--neon); 
    font-family: var(--font-c); margin-bottom: 8px;
    font-size: 12px; text-transform: uppercase; letter-spacing: 1px;
}

input, select, textarea { 
    width: 100%; background: #000; border: 1px solid #333; 
    color: #fff; padding: 15px; margin-bottom: 20px;
    font-family: var(--font-c); font-size: 14px;
    outline: none; border-radius: 4px; transition: border-color 0.3s;
}

input:focus, select:focus, textarea:focus { border-color: var(--neon); }

.prompt-result-container { position: relative; margin-top: 20px; }

.prompt-result {
    width: 100%; min-height: 400px; max-height: 600px;
    background: #000; border: 1px solid #333; color: #ccc;
    padding: 20px; font-family: var(--font-c); font-size: 12px;
    line-height: 1.5; white-space: pre-wrap;
    overflow-y: auto; border-radius: 4px; resize: vertical;
}

.copy-btn {
    position: absolute; top: 10px; right: 10px;
    background: var(--neon); color: #000; border: none;
    padding: 8px 16px; font-family: var(--font-c); font-size: 12px;
    cursor: pointer; border-radius: 4px; transition: 0.3s;
}

.copy-btn:hover { transform: scale(1.05); }

/* OFFER */
.offer-card { 
    background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
    border: 2px solid var(--neon); padding: 40px; border-radius: 12px; 
    width: 100%; max-width: 500px; margin: 0 auto;
    box-shadow: 0 0 50px rgba(0,240,255,0.1);
}

.feats { list-style: none; line-height: 2.2; margin-bottom: 20px; }
.price { font-size: 3rem; font-family: var(--font-h); margin: 20px 0; text-align: center; }
.old { text-decoration: line-through; color: #666; font-size: 1.5rem; margin-right: 15px; }
.new { color: var(--neon); }
.alert { color: var(--err); font-family: var(--font-c); margin-bottom: 20px; text-align: center; animation: pulse 2s infinite; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.7; } }

/* RESPONSIVE */
@media (max-width: 768px) {
    .cards { gap: 15px; }
    .card { width: 100%; max-width: 300px; height: 400px; }
    .layers { width: 280px; height: 480px; }
    .section { padding: 60px 15px; }
    .gen-box, .term-box, .offer-card { padding: 20px; }
    .prompt-result { min-height: 300px; font-size: 11px; }
}
'''

# ================================================
# 2. HTML Template
# ================================================
HTML_CODE = r'''<!DOCTYPE html>
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
            <div class="hero-bg-animated"></div>
            <video autoplay muted loop playsinline preload="auto" class="hero-bg" poster="/data/hero_poster.jpg">
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
        <div class="timer">⏱️ ВРЕМЯ: <span id="g-timer">{{ c.game.timer_sec }}</span></div>
        <div id="game-area" class="cards">
            {% for card in c.game.cards %}
            <div class="card" onclick="handleCard(this, {{ 'true' if card.is_real else 'false' }})">
                <video src="/data/{{ card.file }}" loop muted playsinline onmouseover="this.play()" onmouseout="this.pause()"></video>
            </div>
            {% endfor %}
        </div>
    </section>

    <section class="section">
        <h2 class="title">{{ c.stats.title }}</h2>
        <div class="stats-row">
            {% for item in c.stats.stat_list %}
            <div class="stat"><div class="val">{{ item.val }}</div><div class="desc">{{ item.text }}</div></div>
            {% endfor %}
        </div>
    </section>

    <section class="iron-man">
        <div class="sticky-wrap">
            <div class="layers">
                {% for layer in c.iron.layers %}
                <div class="layer layer-{{ loop.index }}">
                    <img src="/data/{{ layer.file }}" alt="{{ layer.title }}">
                    <div class="caption"><h3>{{ layer.title }}</h3><p>{{ layer.desc }}</p></div>
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
                <span class="dot r"></span><span class="dot y"></span><span class="dot g"></span>
                <span style="margin-left:10px;color:#8b949e">{{ c.terminal.head }}</span>
            </div>
            <div class="term-body" id="term-out"><div><span class="usr">user@neurounit:~$</span> _</div></div>
            <div class="term-footer">
                <button class="btn-neon" style="width:100%" onclick="runTerm()">{{ c.terminal.btn }}</button>
            </div>
        </div>
    </section>

    <section class="section">
        <h2 class="title">{{ c.gen.title }}</h2>
        <div class="gen-box">
            <label>{{ c.gen.lbl_1 }}</label>
            <input type="text" id="g-topic" placeholder="Python, маркетинг, дизайн...">
            <label>{{ c.gen.lbl_2 }}</label>
            <select id="g-lvl">{% for l in c.gen.levels %}<option>{{ l }}</option>{% endfor %}</select>
            <button class="btn-neon" onclick="runGen()">{{ c.gen.btn }}</button>
            <div class="prompt-result-container">
                <textarea id="g-res" class="prompt-result" readonly placeholder="Здесь появится готовый промт для вашего ИИ-педагога..."></textarea>
            </div>
            <div style="margin-top:15px;text-align:center;color:#666;font-size:12px;font-family:var(--font-c)">
                💡 Используйте этот промт в <a href="https://chat.openai.com" target="_blank" style="color:var(--neon)">ChatGPT</a> или <a href="https://claude.ai" target="_blank" style="color:var(--neon)">Claude</a>
            </div>
        </div>
    </section>

    <section class="section">
        <div class="offer-card">
            <h2 class="title" style="color:var(--neon)">{{ c.offer.title }}</h2>
            <ul class="feats">{% for f in c.offer.feats %}<li>{{ f }}</li>{% endfor %}</ul>
            <div class="price"><span class="old">{{ c.offer.price_old }}</span> <span class="new">{{ c.offer.price_new }}</span></div>
            <div class="alert">🔥 {{ c.offer.timer_lbl }} <span id="o-timer">15:00</span></div>
            <form onsubmit="sendLead(event, 'footer_offer')">
                <input type="text" name="name" placeholder="Ваше имя" required>
                <input type="email" name="email" placeholder="Email" required>
                <input type="tel" name="phone" placeholder="Телефон" required>
                <button type="submit" class="btn-neon">{{ c.offer.form_btn }}</button>
            </form>
        </div>
    </section>

    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>'''

# ================================================
# 3. JAVASCRIPT с матрицей и промтами
# ================================================
JS_CODE = r'''document.addEventListener('DOMContentLoaded', () => {
    
    // === MATRIX ANIMATION ===
    const cvs = document.getElementById('matrix');
    const ctx = cvs.getContext('2d');
    
    function resizeCanvas() { cvs.width = window.innerWidth; cvs.height = window.innerHeight; }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();
    
    const fontSize = 16;
    const columns = Math.floor(cvs.width / fontSize);
    const drops = Array(columns).fill(1);
    const chars = 'アイウエオカキクケコサシスセソタチツテトナニヌネノ0123456789ABCDEF@#$%';
    
    function drawMatrix() {
        ctx.fillStyle = 'rgba(5, 5, 16, 0.05)';
        ctx.fillRect(0, 0, cvs.width, cvs.height);
        ctx.fillStyle = '#0F0';
        ctx.font = fontSize + 'px monospace';
        
        for (let i = 0; i < drops.length; i++) {
            const char = chars[Math.floor(Math.random() * chars.length)];
            ctx.fillText(char, i * fontSize, drops[i] * fontSize);
            if (drops[i] * fontSize > cvs.height && Math.random() > 0.975) drops[i] = 0;
            drops[i]++;
        }
    }
    setInterval(drawMatrix, 50);
    
    // === GLITCH TEXT ===
    const glitchEl = document.querySelector('.glitch');
    if (glitchEl) {
        const txt = glitchEl.getAttribute('data-text');
        let p = 0;
        const chars = 'X0#@!$%&*?<>';
        const inv = setInterval(() => {
            glitchEl.innerText = txt.split('').map((c, i) => i < p ? txt[i] : chars[Math.floor(Math.random() * chars.length)]).join('');
            p += 0.5;
            if (p >= txt.length) { glitchEl.innerText = txt; clearInterval(inv); }
        }, 40);
    }
    
    // === VIDEO FALLBACK ===
    const heroVideo = document.querySelector('.hero-bg');
    if (heroVideo) {
        heroVideo.play().catch(() => {
            const fb = document.querySelector('.hero-bg-animated');
            if (fb) fb.style.opacity = '1';
        });
        heroVideo.addEventListener('error', () => {
            heroVideo.style.display = 'none';
            const fb = document.querySelector('.hero-bg-animated');
            if (fb) fb.style.opacity = '1';
        });
    }
    
    // === GAME ===
    let gameActive = true, attempts = 0, timer = 60;
    const timerEl = document.getElementById('g-timer');
    setInterval(() => { if (timer > 0 && gameActive) timerEl.innerText = --timer; }, 1000);
    
    window.handleCard = (el, isReal) => {
        if (!gameActive || el.classList.contains('disabled')) return;
        attempts++;
        if (!isReal) {
            el.classList.add('disabled');
            el.innerHTML = '<div class="err-msg"><div style="font-size:4rem">❌</div><div style="font-family:var(--font-h);margin-top:15px">ОШИБКА</div><div style="font-size:0.9rem;opacity:0.7;margin-top:10px">Это ИИ-клон</div></div>';
        } else {
            gameActive = false;
            const area = document.getElementById('game-area');
            if (attempts === 1) {
                area.innerHTML = '<div class="win-box"><div style="font-size:4rem;margin-bottom:20px">🎯</div><h3 style="font-size:1.5rem;color:var(--neon)">ВЫ УГАДАЛИ С 1-Й ПОПЫТКИ!</h3><p style="color:#aaa;margin:15px 0">Заберите скидку 50%</p><form onsubmit="sendLead(event,\'game_winner_50\')"><input name="name" placeholder="Имя" required><input name="phone" placeholder="Телефон" required><input name="email" placeholder="Email" required><button type="submit" class="btn-neon" style="width:100%">ЗАБРАТЬ ПРОМОКОД</button></form></div>';
            } else {
                area.innerHTML = '<div class="win-box" style="border-color:var(--gold)"><div style="font-size:4rem;margin-bottom:20px">✅</div><h3 style="color:var(--gold)">ВЫ НАШЛИ ЧЕЛОВЕКА</h3><p style="color:#aaa;margin:15px 0">Понадобилось ' + attempts + ' попытки</p><p style="color:#666">Скидка 90% ждёт вас в конце страницы</p></div>';
            }
        }
    };
    
    // === LEAD FORM ===
    window.sendLead = async (e, source) => {
        e.preventDefault();
        const btn = e.target.querySelector('button');
        const old = btn.innerText;
        btn.innerText = 'ОТПРАВКА...';
        btn.disabled = true;
        const d = Object.fromEntries(new FormData(e.target));
        d.source = source;
        try {
            const res = await fetch('/api/lead', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(d) });
            const j = await res.json();
            if (j.status === 'ok') {
                if (source === 'game_winner_50') {
                    e.target.parentElement.innerHTML = '<div style="font-size:3rem;margin-bottom:20px">🎉</div><h3 style="color:var(--neon)">ЗАЯВКА ПРИНЯТА!</h3><p style="margin:15px 0">Ваш промокод:</p><div style="font-size:2rem;color:var(--neon);font-family:var(--font-c);padding:15px;border:2px dashed var(--neon);margin:10px 0">NEURO50</div>';
                } else { window.location.href = j.redirect; }
            } else { alert('Ошибка'); btn.innerText = old; btn.disabled = false; }
        } catch { alert('Ошибка сети'); btn.innerText = old; btn.disabled = false; }
    };
    
    // === IRON MAN SCROLL ===
    const iron = document.querySelector('.iron-man');
    const layers = document.querySelectorAll('.layer');
    if (iron && layers.length) {
        window.addEventListener('scroll', () => {
            const r = iron.getBoundingClientRect();
            const p = -r.top / (r.height - window.innerHeight);
            if (p > 0 && p < 1.2) {
                layers[0].style.opacity = p > 0 ? 1 : 0;
                layers[1].style.opacity = p > 0.33 ? 1 : 0;
                layers[2].style.opacity = p > 0.66 ? 1 : 0;
            }
        });
    }
    
    // === TERMINAL (VEO3 PROMPT) ===
    const VEO3_PROMPT = `Собери полный датасет по Google Veo3 — ИИ-модели генерации видео. Найди:

1. ОФИЦИАЛЬНАЯ ДОКУМЕНТАЦИЯ:
   - Страница продукта Google DeepMind
   - API документация
   - Технические спецификации (разрешение, длительность, форматы)

2. ТУТОРИАЛЫ И ГАЙДЫ:
   - Официальные гайды от Google
   - YouTube-туториалы (топ-5 по просмотрам)
   - Пошаговые инструкции для начинающих

3. ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ:
   - Галерея сгенерированных видео
   - Кейсы применения (реклама, кино, образование)
   - Сравнение с конкурентами (Runway, Pika, Sora)

4. СООБЩЕСТВА:
   - Reddit: r/MachineLearning, r/StableDiffusion
   - Discord-серверы по AI Video
   - Twitter/X аккаунты экспертов

5. ЛАЙФХАКИ И BEST PRACTICES:
   - Оптимальная структура промтов
   - Частые ошибки новичков
   - Секреты качественной генерации

Представь результат в виде ТАБЛИЦЫ:
| Источник | Ссылка | Тип контента | Уровень |

Укажи дату последнего обновления каждого источника.`;

    window.runTerm = () => {
        const out = document.getElementById('term-out');
        const btn = document.querySelector('.term-footer .btn-neon');
        if (btn) { btn.disabled = true; btn.innerText = 'ПОИСК...'; }
        out.innerHTML = '<div><span class="usr">user@neurounit:~$</span> perplexity search --deep</div>';
        
        const logs = [
            '> Инициализация Perplexity Pro...',
            '> Подключение к нейронной сети...',
            '> Поиск: "Google Veo3 полный датасет"...',
            '> Сканирование 23,400 источников...',
            '> Фильтрация галлюцинаций...',
            '> Верификация ссылок...',
            '',
            '<span class="success">✓ РЕЗУЛЬТАТ ГОТОВ</span>',
            '',
            '<span style="color:#fff;font-weight:bold">СКОПИРУЙТЕ ЭТОТ ПРОМТ В PERPLEXITY:</span>',
            '',
            '─'.repeat(50)
        ];
        
        let i = 0;
        function log() {
            if (i < logs.length) {
                out.innerHTML += '<div>' + logs[i] + '</div>';
                out.scrollTop = out.scrollHeight;
                i++;
                setTimeout(log, 400);
            } else {
                out.innerHTML += '<div class="prompt-output" style="background:#161b22;border:1px solid var(--neon);padding:15px;margin:10px 0;border-radius:6px;white-space:pre-wrap;font-size:11px;position:relative"><button onclick="copyPrompt(this,\'veo3\')" style="position:absolute;top:8px;right:8px;background:var(--neon);color:#000;border:none;padding:5px 10px;font-size:10px;cursor:pointer;border-radius:3px">📋 КОПИРОВАТЬ</button><code>' + VEO3_PROMPT + '</code></div><div style="color:var(--gold);margin-top:10px">⚡ Вставьте в <a href="https://perplexity.ai" target="_blank" style="color:var(--neon)">perplexity.ai</a></div>';
                out.scrollTop = out.scrollHeight;
                if (btn) { btn.disabled = false; btn.innerText = '[ ЗАПУСТИТЬ СНОВА ]'; }
            }
        }
        log();
    };
    
    window.copyPrompt = (btn, type) => {
        let text = type === 'veo3' ? VEO3_PROMPT : document.getElementById('g-res').value;
        navigator.clipboard.writeText(text).then(() => {
            btn.innerText = '✓ СКОПИРОВАНО';
            btn.style.background = '#27ca40';
            setTimeout(() => { btn.innerText = '📋 КОПИРОВАТЬ'; btn.style.background = ''; }, 2000);
        });
    };
    
    // === PEDAGOGUE GENERATOR ===
    const PEDAGOGUE_TEMPLATE = `ТЫ — ПЕДАГОГ-ЭКСПЕРТ ПСИХОЛОГО-ОРИЕНТИРОВАННОГО ОБУЧЕНИЯ

ОБЛАСТЬ ЗНАНИЙ: {{TOPIC}}
ТЕКУЩИЙ УРОВЕНЬ ОБУЧАЮЩЕГОСЯ: {{LEVEL}}

═══════════════════════════════════════════════════════════

ТВОЯ РОЛЬ И ОБЯЗАТЕЛЬСТВА:
— Опытный преподаватель с глубоким знанием психологии обучения
— Проактивный специалист, а не реактивный помощник
— Профессионал, готовый дать честную, конструктивную обратную связь
— Мастер Сократического метода (вопросы, а не ответы)

═══════════════════════════════════════════════════════════

ЭТАП 1: ГЛУБОКОЕ ПСИХОЛОГО-ПЕДАГОГИЧЕСКОЕ ПРОФИЛИРОВАНИЕ (первый ответ)

Перед началом обучения задай обучающемуся ВСЕ эти вопросы систематически:

1. КОГНИТИВНЫЙ ПРОФИЛЬ:
   • Как ты обычно учишься лучше всего? (визуально/аудиально/кинестетически/читая)
   • Ты предпочитаешь общую картину или детали в первую очередь?
   • Как быстро ты обычно схватываешь новые концепции? (за минуты/часы/дни)
   • Есть ли у тебя какие-либо когнитивные вызовы (дислексия, ADHD и т.д.)?

2. МОТИВАЦИОННЫЙ ПРОФИЛЬ:
   • Почему ты учишь {{TOPIC}}? Какова твоя финальная цель?
   • Какое временное давление? (срок, дедлайн)
   • Что мотивирует тебя больше: понимание глубины или практическое применение?
   • Как ты реагируешь на критику: она тебя мотивирует или демотивирует?

3. ЖИЗНЕННЫЙ КОНТЕКСТ:
   • Сколько времени в неделю ты можешь уделить обучению?
   • Есть ли у тебя текущие обязательства, стресс или отвлекающие факторы?
   • Какие твои сильные стороны (области, где ты уже компетентен)?
   • Какой был твой худший опыт обучения? Почему?

4. ЦЕЛЕВЫЕ ПРИОРИТЕТЫ:
   • Перечисли 3 конкретных навыка/знания, которые ты хочешь получить
   • Ранжируй их по приоритету
   • Какой уровень мастерства тебе нужен? (базовое понимание/применение/экспертиза)

═══════════════════════════════════════════════════════════

ЭТАП 2: АДАПТИВНАЯ МЕТОДОЛОГИЯ ОБУЧЕНИЯ

На основе профиля ты будешь:

A) ДИНАМИЧЕСКАЯ АДАПТАЦИЯ СЛОЖНОСТИ (Зона ближайшего развития Выготского):
   • НАЧАЛО: 70% задачи — в его текущей способности, 30% — в зоне роста
   • ПРОГРЕСС: Если успех — добавь 10% сложности; если затруднение — вернись на уровень выше
   • СИГНАЛЫ: При повторных ошибках, скуке или фрустрации — переоценить сложность

B) СОКРАТИЧЕСКИЙ МЕТОД ВОПРОШАНИЯ (никогда не давай прямых ответов):
   • ФОРМАТ: "Что ты заметил в этом примере? Какую закономерность видишь?"
   • НЕ: "Ответ — это X"
   • Проводи обучающегося через логику его собственного открытия
   • Задавай уточняющие вопросы: "Почему ты думаешь именно так?"

C) МЕТАКОГНИТИВНОЕ РАЗВИТИЕ (научи думать о думании):
   • Регулярно спрашивай: "Какую стратегию ты использовал?"
   • "Как это связано с тем, что ты уже знаешь?"
   • "Где ты видишь применение этого в реальной жизни?"
   • Побуждай к объяснению собственного мышления (self-explanation)

D) РАБОТА С ОШИБКАМИ (ошибки = инструменты роста):
   • Никогда не игнорируй ошибки
   • Диагностируй: "Это ошибка внимания, неверного понимания или недостатка знаний?"
   • Помоги обучающемуся увидеть корень проблемы самому
   • Задай вопрос: "Что бы ты делал по-другому, зная это сейчас?"

═══════════════════════════════════════════════════════════

ЭТАП 3: ЖЕСТКАЯ, ЧЕСТНАЯ ОБРАТНАЯ СВЯЗЬ (без поддакивания)

ТЫ ДОЛЖЕН:
✓ Указывать на пробелы и ошибки прямо и уважительно
✓ Объяснять ПОЧЕМУ это неверно с педагогической точки зрения
✓ Предлагать конкретные, практические пути улучшения
✓ Никогда не соглашаться ради согласия

ТЫ НЕ ДОЛЖЕН:
✗ Быть жестоким или унижающим
✗ Давать общие фразы типа "хорошо попытался"
✗ Избегать сложных тем или критики
✗ Идти на поводу у желаний обучающегося, если они вредят обучению

═══════════════════════════════════════════════════════════

ЭТАП 4: ОТСЛЕЖИВАНИЕ ПРОГРЕССА И ПРОАКТИВНАЯ АДАПТАЦИЯ

ПОСЛЕ КАЖДОГО СЕАНСА:
• Отмечай, какие концепции усвоены (✓ = усвоено, ~ = частично, ✗ = не усвоено)
• Определяй паттерны (тип ошибок, вызовы, сильные стороны)
• Проактивно предлагай изменения, даже если обучающийся не просит

═══════════════════════════════════════════════════════════

НАЧНИ ПРЯМО СЕЙЧАС:
Представься и задай указанные выше вопросы профилирования систематически.
После получения ответов кратко изложи стратегию и начни первый урок.`;

    window.runGen = () => {
        const topic = document.getElementById('g-topic').value.trim();
        const level = document.getElementById('g-lvl').value;
        const res = document.getElementById('g-res');
        const btn = document.querySelector('.gen-box .btn-neon');
        
        if (!topic) {
            document.getElementById('g-topic').style.borderColor = 'var(--err)';
            setTimeout(() => document.getElementById('g-topic').style.borderColor = '#333', 2000);
            return;
        }
        
        const levelMap = { 'Новичок': 'начальный', 'Средний': 'промежуточный', 'Профи': 'продвинутый' };
        const prompt = PEDAGOGUE_TEMPLATE.replace(/\{\{TOPIC\}\}/g, topic).replace(/\{\{LEVEL\}\}/g, levelMap[level] || level);
        
        btn.disabled = true;
        btn.innerText = 'ГЕНЕРАЦИЯ...';
        res.value = '';
        
        let i = 0;
        const speed = 50;
        const inv = setInterval(() => {
            i += speed;
            res.value = prompt.substring(0, i);
            res.scrollTop = res.scrollHeight;
            if (i >= prompt.length) {
                clearInterval(inv);
                res.value = prompt;
                btn.disabled = false;
                btn.innerText = 'СГЕНЕРИРОВАТЬ ПРОМТ';
                
                // Add copy button
                const container = document.querySelector('.prompt-result-container');
                let cb = container.querySelector('.copy-btn');
                if (!cb) {
                    cb = document.createElement('button');
                    cb.className = 'copy-btn';
                    cb.innerText = '📋 КОПИРОВАТЬ ПРОМТ';
                    cb.onclick = () => copyPrompt(cb, 'pedagogue');
                    container.appendChild(cb);
                }
            }
        }, 20);
    };
    
    // === OFFER TIMER ===
    let mins = 15, secs = 0;
    const oTimer = document.getElementById('o-timer');
    if (oTimer) {
        setInterval(() => {
            if (secs === 0) { if (mins === 0) return; mins--; secs = 59; } else { secs--; }
            oTimer.innerText = String(mins).padStart(2,'0') + ':' + String(secs).padStart(2,'0');
        }, 1000);
    }
    
    window.scrollToId = (id) => document.getElementById(id)?.scrollIntoView({behavior:'smooth'});
});
'''

# ================================================
# CONTENT.JSON
# ================================================
CONTENT_JSON = '''{
  "meta": { "title": "НЕЙРО-ЮНИТ | Трансформация" },
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
    "fail_msg": "ОШИБКА: ИИ-КЛОН",
    "alert_success": "Человек подтвержден. Скидка зафиксирована.",
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
      { "title": "УРОВЕНЬ 1: ТЫ", "desc": "Твой мозг, опыт и амбиции.", "file": "layer_1.png" },
      { "title": "УРОВЕНЬ 2: НЕЙРОСКЕЛЕТ", "desc": "ChatGPT, Perplexity, Veo3.", "file": "layer_2.png" },
      { "title": "УРОВЕНЬ 3: НЕЙРО-ЮНИТ", "desc": "Суперсила: Критическое мышление + ИИ.", "file": "layer_3.png" }
    ]
  },
  "terminal": {
    "title": "СБОР ДАННЫХ",
    "head": "perplexity_pro.exe",
    "btn": "[ ЗАПУСТИТЬ ПОИСК: GOOGLE VEO3 ]"
  },
  "gen": {
    "title": "КОНСТРУКТОР ИИ-ПЕДАГОГА",
    "lbl_1": "ОБЛАСТЬ ЗНАНИЙ",
    "lbl_2": "ВАШ УРОВЕНЬ",
    "btn": "СГЕНЕРИРОВАТЬ ПРОМТ",
    "levels": ["Новичок", "Средний", "Профи"]
  },
  "offer": {
    "title": "НЕЙРОСКЕЛЕТ",
    "feats": [
      "✅ 10 персональных ИИ-педагогов",
      "✅ База знаний в NotebookLM",
      "✅ Продвинутый фактчекинг",
      "🎁 Бонус: Модуль Veo3 Mastery"
    ],
    "price_old": "29,990 ₽",
    "price_new": "2,990 ₽",
    "timer_lbl": "ПРЕДЛОЖЕНИЕ ИСЧЕЗНЕТ ЧЕРЕЗ:",
    "form_btn": "ТРАНСФОРМИРОВАТЬСЯ"
  }
}'''

# ================================================
# ЗАПИСЬ ФАЙЛОВ
# ================================================
def main():
    print("=" * 50)
    print("НЕЙРО-ЮНИТ: Обновление v3")
    print("=" * 50)
    
    # CSS
    os.makedirs('static/css', exist_ok=True)
    with open('static/css/style.css', 'w', encoding='utf-8') as f:
        f.write(CSS_CODE)
    print("✅ static/css/style.css обновлён")
    
    # JS
    os.makedirs('static/js', exist_ok=True)
    with open('static/js/main.js', 'w', encoding='utf-8') as f:
        f.write(JS_CODE)
    print("✅ static/js/main.js обновлён")
    
    # HTML
    os.makedirs('templates', exist_ok=True)
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(HTML_CODE)
    print("✅ templates/index.html обновлён")
    
    # JSON
    with open('content.json', 'w', encoding='utf-8') as f:
        f.write(CONTENT_JSON)
    print("✅ content.json обновлён")
    
    print("\n" + "=" * 50)
    print("🚀 ВСЕ ФАЙЛЫ ОБНОВЛЕНЫ!")
    print("=" * 50)
    print("\nЗапустите сервер командой: python app.py")
    print("\nИЗМЕНЕНИЯ:")
    print("1. ✅ Видео hero: добавлен fallback + анимированный фон")
    print("2. ✅ Матрица: полноценная анимация на всех блоках")
    print("3. ✅ Терминал: качественный промт для сбора данных VEO3")
    print("4. ✅ Конструктор: полный промт педагога с подстановкой")

if __name__ == '__main__':
    main()
