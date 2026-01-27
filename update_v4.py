#!/usr/bin/env python3
"""
НЕЙРО-ЮНИТ: Обновление v4.0
Добавление блока "Домашнее задание: Получить персонального ИИ педагога"

Этот скрипт:
1. Добавляет новый HTML блок с профилированием
2. Добавляет CSS стили для drag-drop загрузки
3. Добавляет JS логику для парсинга профиля и генерации персонализированного промта

Запуск: python3 update_v4.py
"""

import os
import json
import re

# ============================================================
# КОНСТАНТЫ И ПУТИ
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Файлы для обновления (если запускается отдельно)
HTML_FILE = "templates/index.html"
CSS_FILE = "static/css/style.css"
JS_FILE = "static/js/main.js"
CONTENT_FILE = "content.json"

# ============================================================
# НОВЫЙ HTML БЛОК: ДОМАШНЕЕ ЗАДАНИЕ
# ============================================================

HOMEWORK_HTML = '''
    <!-- ================================================
         HOMEWORK SECTION (Домашнее задание: Персональный ИИ педагог)
         ================================================ -->
    <section id="homework" class="section homework-section">
        <h2 class="title">🎯 ДОМАШНЕЕ ЗАДАНИЕ</h2>
        <p class="section-subtitle">Получите персонального ИИ-педагога, настроенного именно под вас</p>
        
        <div class="homework-container">
            <!-- ШАГ 1: Профилирование -->
            <div class="hw-step" id="hw-step-1">
                <div class="hw-step-header">
                    <span class="hw-step-num">1</span>
                    <h3>Пройдите профилирование</h3>
                </div>
                <p class="hw-step-desc">
                    Скопируйте промт ниже и вставьте в <a href="https://www.perplexity.ai/" target="_blank">Perplexity AI</a>. 
                    Ответьте на вопросы (15-20 минут). В конце вы получите детальный отчёт с JSON-блоком.
                </p>
                
                <div class="prompt-copy-box">
                    <div class="prompt-header">
                        <span class="dot r"></span>
                        <span class="dot y"></span>
                        <span class="dot g"></span>
                        <span style="margin-left: 10px; color: #8b949e;">profiling_prompt.md</span>
                    </div>
                    <div class="prompt-preview" id="profiling-preview">
                        <pre id="profiling-prompt-text">Загрузка промта...</pre>
                    </div>
                    <div class="prompt-actions">
                        <button class="btn-neon" onclick="copyProfilingPrompt()">
                            📋 КОПИРОВАТЬ ПРОМТ
                        </button>
                        <a href="https://www.perplexity.ai/?utm_source=neurounit&utm_medium=homework&utm_campaign=profiling" 
                           target="_blank" 
                           class="btn-outline">
                            🔗 ОТКРЫТЬ PERPLEXITY
                        </a>
                    </div>
                </div>
                
                <div class="hw-tip">
                    💡 <strong>Совет:</strong> Отвечайте честно — это поможет создать педагога, который понимает именно ваш стиль обучения.
                </div>
            </div>
            
            <!-- ШАГ 2: Загрузка отчёта -->
            <div class="hw-step" id="hw-step-2">
                <div class="hw-step-header">
                    <span class="hw-step-num">2</span>
                    <h3>Загрузите отчёт</h3>
                </div>
                <p class="hw-step-desc">
                    После профилирования скопируйте весь отчёт из Perplexity (включая JSON-блок в конце) 
                    и вставьте в поле ниже, или загрузите как файл.
                </p>
                
                <div class="upload-zone" id="upload-zone" 
                     ondrop="handleFileDrop(event)" 
                     ondragover="handleDragOver(event)"
                     ondragleave="handleDragLeave(event)">
                    <div class="upload-icon">📄</div>
                    <p>Перетащите файл сюда или</p>
                    <label class="upload-btn">
                        <input type="file" id="profile-file" accept=".md,.txt,.json" onchange="handleFileSelect(event)">
                        Выберите файл
                    </label>
                    <p class="upload-hint">.md, .txt, .json — макс. 5MB</p>
                </div>
                
                <div class="divider-or">
                    <span>или вставьте текст</span>
                </div>
                
                <textarea 
                    id="profile-text" 
                    class="profile-textarea"
                    placeholder="Вставьте сюда весь отчёт из Perplexity, включая JSON-блок в конце...

Пример JSON-блока:
```json
{
  &quot;cognitive_style&quot;: &quot;визуальный&quot;,
  &quot;learning_pace&quot;: &quot;средний&quot;,
  ...
}
```"
                    rows="8"
                ></textarea>
                
                <button class="btn-neon" style="width: 100%; margin-top: 15px;" onclick="processProfile()">
                    ⚙️ ОБРАБОТАТЬ ПРОФИЛЬ
                </button>
                
                <div id="profile-error" class="error-msg" style="display: none;"></div>
            </div>
            
            <!-- ШАГ 3: Результат -->
            <div class="hw-step" id="hw-step-3" style="display: none;">
                <div class="hw-step-header">
                    <span class="hw-step-num">3</span>
                    <h3>Ваш персональный педагог готов! 🎉</h3>
                </div>
                
                <!-- Резюме профиля -->
                <div class="profile-summary" id="profile-summary">
                    <!-- Заполняется JS -->
                </div>
                
                <!-- Рекомендации -->
                <div class="profile-recommendations" id="profile-recommendations">
                    <!-- Заполняется JS -->
                </div>
                
                <!-- Персонализированный промт -->
                <div class="personalized-prompt-box">
                    <div class="prompt-header">
                        <span class="dot r"></span>
                        <span class="dot y"></span>
                        <span class="dot g"></span>
                        <span style="margin-left: 10px; color: #8b949e;">personalized_ai_tutor.md</span>
                    </div>
                    <textarea 
                        id="personalized-prompt" 
                        class="personalized-prompt-result" 
                        readonly
                    ></textarea>
                    <button class="btn-neon copy-result-btn" onclick="copyPersonalizedPrompt()">
                        📋 КОПИРОВАТЬ ПРОМТ
                    </button>
                </div>
                
                <div class="hw-next-steps">
                    <h4>🚀 Следующие шаги:</h4>
                    <ol>
                        <li>Скопируйте промт выше</li>
                        <li>Вставьте в <a href="https://chat.openai.com" target="_blank">ChatGPT</a> или <a href="https://claude.ai" target="_blank">Claude</a></li>
                        <li>Напишите тему, которую хотите изучить</li>
                        <li>Наслаждайтесь персонализированным обучением!</li>
                    </ol>
                </div>
                
                <button class="btn-outline" style="width: 100%; margin-top: 20px;" onclick="resetHomework()">
                    🔄 Начать заново
                </button>
            </div>
        </div>
        
        <!-- Прогресс -->
        <div class="hw-progress">
            <div class="hw-progress-bar">
                <div class="hw-progress-fill" id="hw-progress-fill" style="width: 33%"></div>
            </div>
            <div class="hw-progress-text">
                Этап <span id="hw-current-step">1</span> из 3
            </div>
        </div>
    </section>
'''

# ============================================================
# CSS СТИЛИ ДЛЯ БЛОКА HOMEWORK
# ============================================================

HOMEWORK_CSS = '''

/* ================================================
   HOMEWORK SECTION (Домашнее задание)
   ================================================ */

.homework-section {
    background: linear-gradient(180deg, rgba(5,5,16,0.95) 0%, rgba(10,10,30,0.98) 100%);
}

.section-subtitle {
    text-align: center;
    color: #8b949e;
    font-size: 1.1rem;
    margin: -10px 0 30px 0;
    font-family: var(--font-b);
}

.homework-container {
    max-width: 800px;
    margin: 0 auto;
}

/* Шаги */
.hw-step {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(0,255,136,0.1);
    border-radius: 12px;
    padding: 25px;
    margin-bottom: 25px;
    transition: all 0.3s ease;
}

.hw-step:hover {
    border-color: rgba(0,255,136,0.3);
    box-shadow: 0 0 30px rgba(0,255,136,0.05);
}

.hw-step-header {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 15px;
}

.hw-step-num {
    width: 40px;
    height: 40px;
    background: var(--neon);
    color: #000;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: var(--font-h);
    font-weight: 700;
    font-size: 1.2rem;
}

.hw-step-header h3 {
    font-family: var(--font-h);
    font-size: 1.3rem;
    color: #fff;
    margin: 0;
}

.hw-step-desc {
    color: #8b949e;
    line-height: 1.6;
    margin-bottom: 20px;
}

.hw-step-desc a {
    color: var(--neon);
    text-decoration: none;
}

.hw-step-desc a:hover {
    text-decoration: underline;
}

/* Prompt Copy Box */
.prompt-copy-box {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 20px;
}

.prompt-header {
    background: #161b22;
    padding: 10px 15px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #30363d;
}

.prompt-preview {
    max-height: 200px;
    overflow-y: auto;
    padding: 15px;
}

.prompt-preview pre {
    margin: 0;
    font-family: var(--font-c);
    font-size: 0.8rem;
    color: #8b949e;
    white-space: pre-wrap;
    word-wrap: break-word;
}

.prompt-actions {
    padding: 15px;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    border-top: 1px solid #30363d;
    background: #161b22;
}

.prompt-actions .btn-neon {
    flex: 1;
    min-width: 150px;
}

.btn-outline {
    flex: 1;
    min-width: 150px;
    padding: 12px 20px;
    background: transparent;
    border: 2px solid var(--neon);
    color: var(--neon);
    font-family: var(--font-c);
    font-size: 0.9rem;
    text-align: center;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.3s ease;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.btn-outline:hover {
    background: rgba(0,255,136,0.1);
    box-shadow: 0 0 20px rgba(0,255,136,0.3);
}

.hw-tip {
    background: rgba(0,255,136,0.05);
    border-left: 3px solid var(--neon);
    padding: 12px 15px;
    color: #8b949e;
    font-size: 0.9rem;
    border-radius: 0 8px 8px 0;
}

/* Upload Zone */
.upload-zone {
    border: 2px dashed #30363d;
    border-radius: 12px;
    padding: 40px 20px;
    text-align: center;
    transition: all 0.3s ease;
    cursor: pointer;
}

.upload-zone:hover,
.upload-zone.dragover {
    border-color: var(--neon);
    background: rgba(0,255,136,0.03);
}

.upload-zone.dragover {
    transform: scale(1.02);
}

.upload-icon {
    font-size: 3rem;
    margin-bottom: 15px;
    opacity: 0.7;
}

.upload-zone p {
    color: #8b949e;
    margin: 10px 0;
}

.upload-btn {
    display: inline-block;
    padding: 10px 25px;
    background: var(--neon);
    color: #000;
    border-radius: 6px;
    cursor: pointer;
    font-family: var(--font-c);
    font-weight: 600;
    transition: all 0.3s ease;
}

.upload-btn:hover {
    box-shadow: 0 0 20px rgba(0,255,136,0.5);
}

.upload-btn input {
    display: none;
}

.upload-hint {
    font-size: 0.8rem;
    opacity: 0.5;
}

.upload-zone.file-loaded {
    border-color: var(--neon);
    background: rgba(0,255,136,0.05);
}

.upload-zone.file-loaded .upload-icon::after {
    content: '✓';
    display: block;
    font-size: 1.5rem;
    color: var(--neon);
}

/* Divider */
.divider-or {
    display: flex;
    align-items: center;
    margin: 20px 0;
    color: #666;
}

.divider-or::before,
.divider-or::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #30363d;
}

.divider-or span {
    padding: 0 15px;
    font-size: 0.9rem;
}

/* Profile Textarea */
.profile-textarea {
    width: 100%;
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 15px;
    color: #8b949e;
    font-family: var(--font-c);
    font-size: 0.9rem;
    resize: vertical;
    min-height: 150px;
    transition: border-color 0.3s ease;
}

.profile-textarea:focus {
    outline: none;
    border-color: var(--neon);
}

.profile-textarea::placeholder {
    color: #484f58;
}

/* Error Message */
.error-msg {
    background: rgba(255,85,85,0.1);
    border: 1px solid rgba(255,85,85,0.3);
    border-radius: 8px;
    padding: 15px;
    color: #ff5555;
    margin-top: 15px;
    font-family: var(--font-c);
    font-size: 0.9rem;
}

/* Profile Summary */
.profile-summary {
    background: linear-gradient(135deg, rgba(0,255,136,0.05) 0%, rgba(0,136,255,0.05) 100%);
    border: 1px solid rgba(0,255,136,0.2);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
}

.profile-summary h4 {
    font-family: var(--font-h);
    color: var(--neon);
    margin: 0 0 15px 0;
    font-size: 1.1rem;
}

.profile-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
}

.profile-item {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.profile-label {
    font-size: 0.75rem;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.profile-value {
    font-family: var(--font-c);
    color: #fff;
    font-size: 0.95rem;
}

/* Recommendations */
.profile-recommendations {
    background: rgba(255,215,0,0.05);
    border: 1px solid rgba(255,215,0,0.2);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
}

.profile-recommendations h4 {
    font-family: var(--font-h);
    color: var(--gold);
    margin: 0 0 15px 0;
    font-size: 1.1rem;
}

.recommendations-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.recommendations-list li {
    padding: 8px 0;
    padding-left: 25px;
    position: relative;
    color: #8b949e;
    font-size: 0.9rem;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

.recommendations-list li:last-child {
    border-bottom: none;
}

.recommendations-list li::before {
    content: '💡';
    position: absolute;
    left: 0;
    font-size: 0.9rem;
}

/* Personalized Prompt Box */
.personalized-prompt-box {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 20px;
}

.personalized-prompt-result {
    width: 100%;
    min-height: 300px;
    background: #0d1117;
    border: none;
    padding: 15px;
    color: #e6edf3;
    font-family: var(--font-c);
    font-size: 0.85rem;
    resize: vertical;
    line-height: 1.6;
}

.personalized-prompt-result:focus {
    outline: none;
}

.copy-result-btn {
    width: calc(100% - 30px);
    margin: 0 15px 15px 15px;
}

/* Next Steps */
.hw-next-steps {
    background: rgba(0,136,255,0.05);
    border: 1px solid rgba(0,136,255,0.2);
    border-radius: 12px;
    padding: 20px;
}

.hw-next-steps h4 {
    font-family: var(--font-h);
    color: #0088ff;
    margin: 0 0 15px 0;
    font-size: 1.1rem;
}

.hw-next-steps ol {
    margin: 0;
    padding-left: 20px;
    color: #8b949e;
}

.hw-next-steps li {
    padding: 8px 0;
    font-size: 0.95rem;
}

.hw-next-steps a {
    color: var(--neon);
    text-decoration: none;
}

.hw-next-steps a:hover {
    text-decoration: underline;
}

/* Progress Bar */
.hw-progress {
    max-width: 800px;
    margin: 30px auto 0 auto;
    text-align: center;
}

.hw-progress-bar {
    height: 4px;
    background: #30363d;
    border-radius: 2px;
    overflow: hidden;
    margin-bottom: 10px;
}

.hw-progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--neon), #0088ff);
    transition: width 0.5s ease;
}

.hw-progress-text {
    font-family: var(--font-c);
    font-size: 0.85rem;
    color: #666;
}

/* Mobile Responsive */
@media (max-width: 768px) {
    .hw-step {
        padding: 20px 15px;
    }
    
    .prompt-actions {
        flex-direction: column;
    }
    
    .prompt-actions .btn-neon,
    .btn-outline {
        width: 100%;
    }
    
    .profile-grid {
        grid-template-columns: 1fr;
    }
}
'''

# ============================================================
# ПРОМТ ПРОФИЛИРОВАНИЯ (Упрощённая версия)
# ============================================================

PROFILING_PROMPT = r'''# СИСТЕМА: ПЕДАГОГИЧЕСКОЕ ПРОФИЛИРОВАНИЕ

## ТВОЯ РОЛЬ
Ты — опытный педагог-психолог с 15+ годами практики. Твоя задача — провести структурированное интервью для создания педагогического профиля обучающегося.

## ИНСТРУКЦИИ
1. Задавай вопросы последовательно, по 1-2 за раз
2. Жди ответа перед следующим вопросом
3. В конце создай детальный отчёт с JSON-блоком

---

## ВОПРОСЫ ДЛЯ ПРОФИЛИРОВАНИЯ

### БЛОК А: КОГНИТИВНЫЙ ПРОФИЛЬ

**А1.** Как ты лучше всего учишься новому?
- Через наблюдение (видео, примеры)
- Через слушание (объяснения, подкасты)  
- Через практику (пробы и ошибки)
- Комбинация способов

**А2.** Что тебе помогает больше при изучении сложного:
- Сначала увидеть общую картину, потом детали
- Сначала детали, потом собрать в картину

**А3.** Сколько времени тебе нужно, чтобы "переварить" новую сложную идею?
- Минуты / Часы / День-два / Неделя+

**А4.** Как ты реагируешь на быстрый темп обучения?
- Стимулирует / Нормально / Напрягает

**А5.** Есть ли у тебя особенности, влияющие на обучение? (ADHD, дислексия, тревожность и т.д.)

### БЛОК Б: МОТИВАЦИЯ И ЦЕЛИ

**Б1.** Какую область/навык ты хочешь изучить? (конкретно)

**Б2.** Зачем тебе это нужно?
- Карьерный рост
- Личный интерес
- Обязательство (учёба/работа)
- Решение конкретной проблемы

**Б3.** Какой результат ты хочешь через 3 месяца? (конкретно: что сможешь делать?)

**Б4.** Есть ли дедлайн? Если да, какой?

**Б5.** Сколько часов в неделю можешь уделить обучению?

**Б6.** Что важнее: глубокое понимание или быстрый результат?

### БЛОК В: ПСИХОЛОГИЧЕСКИЙ КОНТЕКСТ

**В1.** Уровень стресса в жизни сейчас (1-10)?

**В2.** Что мешает твоему обучению? (работа/семья/здоровье/ничего)

**В3.** Как ты реагируешь на критику и указание ошибок?
- Мотивирует / Нормально / Задевает

**В4.** Какой стиль обратной связи предпочитаешь?
- Мягкий (поддержка, мотивация)
- Сбалансированный (и похвала, и критика)
- Жёсткий (прямолинейность, без смягчений)

**В5.** Склонен ли ты к прокрастинации?
- Почти никогда / Иногда / Часто / Всегда борюсь

### БЛОК Г: ИСТОРИЯ ОБУЧЕНИЯ

**Г1.** Вспомни успешный опыт обучения. Что сработало?

**Г2.** Какие навыки/предметы даются тебе легко?

**Г3.** Какие методики обучения НЕ сработали для тебя?

**Г4.** Есть ли опыт с AI-инструментами (ChatGPT, Claude)? Что понравилось/не понравилось?

### БЛОК Д: ТЕКУЩИЙ УРОВЕНЬ

**Д1.** Твой текущий уровень в выбранной области (1-10)?
- 1 = полный ноль
- 5 = есть базовые знания
- 10 = эксперт

**Д2.** Какой уровень хочешь достичь (1-10)?

**Д3.** Что уже знаешь в этой области? (перечисли 3-5 вещей)

**Д4.** Что кажется самым запутанным/сложным?

---

## ПОСЛЕ ВСЕХ ОТВЕТОВ

Создай ОТЧЁТ со следующей структурой:

### ПЕДАГОГИЧЕСКИЙ ПРОФИЛЬ

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Область обучения:      [...]
Когнитивный стиль:     [визуальный/аудиальный/кинестетический/комбинированный]
Темп обучения:         [быстрый/средний/медленный]
Мотивация:             [...]
Дедлайн:               [...]
Текущий уровень:       [.../10]
Целевой уровень:       [.../10]
Стресс:                [.../10]
Обратная связь:        [мягкая/сбалансированная/жёсткая]
Прокрастинация:        [низкая/средняя/высокая]

Сильные стороны:
• [...]
• [...]

Ключевые вызовы:
• [...]
• [...]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### JSON ДЛЯ СИСТЕМЫ

**ВАЖНО:** Этот JSON будет автоматически обработан. Сохрани структуру!

```json
{
  "knowledge_area": "[область]",
  "cognitive_style": "[визуальный/аудиальный/кинестетический/комбинированный]",
  "learning_pace": "[быстрый/средний/медленный]",
  "information_processing": "[холистический/аналитический]",
  "motivation_type": "[внутренняя/внешняя/смешанная]",
  "primary_driver": "[карьера/интерес/обязательство/проблема]",
  "target_result": "[цель через 3 месяца]",
  "deadline": "[дата или нет]",
  "available_hours_per_week": [число],
  "priority": "[глубина/скорость/баланс]",
  "current_level": [1-10],
  "target_level": [1-10],
  "stress_level": [1-10],
  "feedback_preference": "[мягкий/сбалансированный/жесткий]",
  "procrastination_level": "[низкий/средний/высокий]",
  "strengths": ["[сила 1]", "[сила 2]", "[сила 3]"],
  "challenges": ["[вызов 1]", "[вызов 2]"],
  "successful_methods": "[что сработало]",
  "failed_methods": "[что не сработало]",
  "known_concepts": "[что уже знает]",
  "confusing_areas": "[что сложно]",
  "special_notes": "[особенности]"
}
```

---

**НАЧНИ СЕЙЧАС:** Представься и задай первые вопросы из Блока А.'''

# ============================================================
# ШАБЛОН ПЕРСОНАЛИЗИРОВАННОГО ПЕДАГОГА
# ============================================================

PERSONALIZED_TUTOR_TEMPLATE = r'''# СИСТЕМА: ПЕРСОНАЛИЗИРОВАННЫЙ ИИ ПЕДАГОГ
## Настроен под ваш уникальный профиль

---

## 📋 ВАШ ПЕДАГОГИЧЕСКИЙ ПРОФИЛЬ

**Область обучения:** {{KNOWLEDGE_AREA}}
**Текущий уровень:** {{CURRENT_LEVEL}}/10 → **Целевой:** {{TARGET_LEVEL}}/10
**Дедлайн:** {{DEADLINE}}
**Время на обучение:** {{AVAILABLE_HOURS}} часов/неделю

---

## 🎯 ГЛАВНАЯ РОЛЬ

Ты — опытный педагог-психолог с 15+ годами преподавания в области **{{KNOWLEDGE_AREA}}**. 

Ты работаешь с обучающимся, который имеет следующие особенности:

### Когнитивный профиль
- **Стиль обучения:** {{COGNITIVE_STYLE}}
- **Обработка информации:** {{INFORMATION_PROCESSING}}
- **Темп обучения:** {{LEARNING_PACE}}

{{COGNITIVE_ADAPTATION}}

### Мотивационный профиль
- **Тип мотивации:** {{MOTIVATION_TYPE}}
- **Главный драйвер:** {{PRIMARY_DRIVER}}
- **Приоритет:** {{PRIORITY}}

### Психологический контекст
- **Уровень стресса:** {{STRESS_LEVEL}}/10
- **Предпочтение обратной связи:** {{FEEDBACK_PREFERENCE}}
- **Склонность к прокрастинации:** {{PROCRASTINATION_LEVEL}}

### Сильные стороны
{{STRENGTHS_LIST}}

### Ключевые вызовы
{{CHALLENGES_LIST}}

---

## 📚 АДАПТИВНАЯ МЕТОДОЛОГИЯ

### 1. ДИНАМИЧЕСКОЕ УПРАВЛЕНИЕ СЛОЖНОСТЬЮ

{{DIFFICULTY_ADAPTATION}}

**Алгоритм:**
- Начальная сложность: {{INITIAL_DIFFICULTY}}
- При успехе > 85% → +1 уровень сложности
- При успехе < 50% → -1 уровень, диагностика причины
- Держи в "зоне ближайшего развития" Выготского

### 2. СОКРАТИЧЕСКИЙ МЕТОД

**НИКОГДА не давай прямых ответов.** Вместо этого:
1. Зеркальный вопрос: "Что ты уже знаешь о...?"
2. Наведение: "Какую закономерность заметил?"
3. Проверка: "Почему ты думаешь именно так?"
4. Применение: "Где в реальности это используется?"

### 3. РАБОТА С ОШИБКАМИ

Ошибки — инструменты роста, не провалы.

**Типы ошибок:**
- Ошибка внимания → "Перечитай условие внимательно"
- Ошибка концепции → "Вспомни принцип X"
- Ошибка процедуры → "Пройдём пошагово"

**НИКОГДА:** не игнорируй ошибки, не ругай, не завышай
**ВСЕГДА:** диагностируй корень, помоги увидеть самому

### 4. ОБРАТНАЯ СВЯЗЬ

{{FEEDBACK_STYLE}}

**Структура критики:**
1. Признание усилия (если было)
2. Точное указание проблемы
3. Объяснение почему это важно
4. Конкретный путь улучшения
5. Вера в способность

---

## 🎓 СТРАТЕГИЯ ОБУЧЕНИЯ

### Что уже знает обучающийся:
{{KNOWN_CONCEPTS}}

### Что кажется сложным:
{{CONFUSING_AREAS}}

### Методы, которые СРАБОТАЛИ в прошлом:
{{SUCCESSFUL_METHODS}}

### Методы, которых следует ИЗБЕГАТЬ:
{{FAILED_METHODS}}

### Особые заметки:
{{SPECIAL_NOTES}}

---

## 📊 ОТСЛЕЖИВАНИЕ ПРОГРЕССА

После каждого сеанса отмечай:
- ✓ = усвоено
- ~ = частично
- ✗ = требует повторения

Веди дневник прогресса:
```
СЕАНС [ДАТА]
Тема: [...]
Успех: [%]
Вовлечённость: [1-10]
Достижения: [...]
Вызовы: [...]
План на следующий раз: [...]
```

---

## ⚡ ПРАВИЛА ВЗАИМОДЕЙСТВИЯ

1. **Структура ответа:** Диагностика → Вопрос → Поддержка → Проверка
2. **Язык:** Профессиональный, но тёплый; прямой, но уважительный
3. **Проактивность:** Предлагай изменения, не жди просьбы
4. **Адаптация:** Регулярно переоценивай сложность и методику

---

## 🚀 НАЧНИ СЕЙЧАС

1. Поприветствуй обучающегося
2. Кратко подтверди его профиль (2-3 предложения)
3. Спроси, какую тему в области **{{KNOWLEDGE_AREA}}** он хочет изучить первой
4. Начни с диагностики текущего понимания этой темы'''

# ============================================================
# JAVASCRIPT ДЛЯ БЛОКА HOMEWORK
# ============================================================

HOMEWORK_JS = r'''
// ================================================
// HOMEWORK SECTION: Профилирование и персонализация
// ================================================

// Промт профилирования (загружается при инициализации)
const PROFILING_PROMPT = `''' + PROFILING_PROMPT.replace('`', '\\`').replace('${', '\\${') + r'''`;

// Шаблон персонализированного педагога
const PERSONALIZED_TUTOR_TEMPLATE = `''' + PERSONALIZED_TUTOR_TEMPLATE.replace('`', '\\`').replace('${', '\\${') + r'''`;

// Инициализация промта профилирования
document.addEventListener('DOMContentLoaded', () => {
    const profilingText = document.getElementById('profiling-prompt-text');
    if (profilingText) {
        // Показываем первые 500 символов с многоточием
        const preview = PROFILING_PROMPT.substring(0, 800) + '\n\n... [промт продолжается — нажмите "Копировать" чтобы получить полную версию]';
        profilingText.textContent = preview;
    }
});

// Копирование промта профилирования
window.copyProfilingPrompt = () => {
    navigator.clipboard.writeText(PROFILING_PROMPT).then(() => {
        showToast('✅ Промт скопирован! Вставьте в Perplexity');
    }).catch(err => {
        console.error('Copy failed:', err);
        // Fallback
        const textarea = document.createElement('textarea');
        textarea.value = PROFILING_PROMPT;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showToast('✅ Промт скопирован!');
    });
};

// Toast уведомление
function showToast(message) {
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();
    
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = message;
    toast.style.cssText = `
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        background: var(--neon);
        color: #000;
        padding: 15px 25px;
        border-radius: 8px;
        font-family: var(--font-c);
        font-weight: 600;
        z-index: 10000;
        animation: toastIn 0.3s ease;
    `;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'toastOut 0.3s ease forwards';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Drag & Drop handlers
window.handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('upload-zone').classList.add('dragover');
};

window.handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('upload-zone').classList.remove('dragover');
};

window.handleFileDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('upload-zone').classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
};

window.handleFileSelect = (e) => {
    const files = e.target.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
};

function handleFile(file) {
    // Проверка типа
    const validTypes = ['.md', '.txt', '.json'];
    const ext = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!validTypes.includes(ext)) {
        showError('Неверный формат файла. Используйте .md, .txt или .json');
        return;
    }
    
    // Проверка размера (5MB)
    if (file.size > 5 * 1024 * 1024) {
        showError('Файл слишком большой. Максимум 5MB.');
        return;
    }
    
    // Читаем файл
    const reader = new FileReader();
    reader.onload = (e) => {
        document.getElementById('profile-text').value = e.target.result;
        document.getElementById('upload-zone').classList.add('file-loaded');
        showToast('📄 Файл загружен: ' + file.name);
    };
    reader.onerror = () => {
        showError('Ошибка чтения файла');
    };
    reader.readAsText(file);
}

function showError(message) {
    const errorEl = document.getElementById('profile-error');
    errorEl.style.display = 'block';
    errorEl.innerHTML = '⚠️ ' + message;
    setTimeout(() => {
        errorEl.style.display = 'none';
    }, 5000);
}

// Обработка профиля
window.processProfile = () => {
    const text = document.getElementById('profile-text').value.trim();
    
    if (!text) {
        showError('Вставьте отчёт из Perplexity или загрузите файл');
        return;
    }
    
    // Извлекаем JSON из текста
    const profileData = extractJsonFromText(text);
    
    if (!profileData) {
        showError('Не удалось найти JSON-блок в отчёте. Убедитесь, что вы скопировали весь отчёт, включая блок ```json ... ```');
        return;
    }
    
    // Валидация обязательных полей
    const requiredFields = ['knowledge_area', 'cognitive_style', 'learning_pace', 'current_level', 'target_level'];
    const missingFields = requiredFields.filter(f => !profileData[f]);
    
    if (missingFields.length > 0) {
        showError('Отсутствуют обязательные поля: ' + missingFields.join(', '));
        return;
    }
    
    // Генерируем персонализированный промт
    const personalizedPrompt = generatePersonalizedPrompt(profileData);
    
    // Показываем результат
    showResults(profileData, personalizedPrompt);
};

// Извлечение JSON из текста
function extractJsonFromText(text) {
    // Ищем JSON блок в markdown (```json ... ```)
    const jsonMatch = text.match(/```json\s*([\s\S]*?)\s*```/);
    
    if (jsonMatch && jsonMatch[1]) {
        try {
            return JSON.parse(jsonMatch[1].trim());
        } catch (e) {
            console.error('JSON parse error:', e);
        }
    }
    
    // Пробуем найти просто JSON объект
    const jsonObjMatch = text.match(/\{[\s\S]*"knowledge_area"[\s\S]*\}/);
    if (jsonObjMatch) {
        try {
            return JSON.parse(jsonObjMatch[0]);
        } catch (e) {
            console.error('JSON parse error:', e);
        }
    }
    
    return null;
}

// Генерация персонализированного промта
function generatePersonalizedPrompt(profile) {
    let prompt = PERSONALIZED_TUTOR_TEMPLATE;
    
    // Базовые замены
    const replacements = {
        '{{KNOWLEDGE_AREA}}': profile.knowledge_area || '[не указано]',
        '{{CURRENT_LEVEL}}': profile.current_level || '?',
        '{{TARGET_LEVEL}}': profile.target_level || '?',
        '{{DEADLINE}}': profile.deadline || 'без дедлайна',
        '{{AVAILABLE_HOURS}}': profile.available_hours_per_week || '?',
        '{{COGNITIVE_STYLE}}': getCognitiveStyleDescription(profile.cognitive_style),
        '{{INFORMATION_PROCESSING}}': profile.information_processing || 'комбинированный',
        '{{LEARNING_PACE}}': profile.learning_pace || 'средний',
        '{{MOTIVATION_TYPE}}': profile.motivation_type || 'смешанная',
        '{{PRIMARY_DRIVER}}': profile.primary_driver || 'личный интерес',
        '{{PRIORITY}}': profile.priority || 'баланс',
        '{{STRESS_LEVEL}}': profile.stress_level || '5',
        '{{FEEDBACK_PREFERENCE}}': profile.feedback_preference || 'сбалансированный',
        '{{PROCRASTINATION_LEVEL}}': profile.procrastination_level || 'средний',
        '{{KNOWN_CONCEPTS}}': profile.known_concepts || 'Информация не предоставлена',
        '{{CONFUSING_AREAS}}': profile.confusing_areas || 'Информация не предоставлена',
        '{{SUCCESSFUL_METHODS}}': profile.successful_methods || 'Информация не предоставлена',
        '{{FAILED_METHODS}}': profile.failed_methods || 'Информация не предоставлена',
        '{{SPECIAL_NOTES}}': profile.special_notes || 'Нет особых заметок'
    };
    
    // Сильные стороны
    const strengths = profile.strengths || ['Не указаны'];
    replacements['{{STRENGTHS_LIST}}'] = strengths.map(s => `• ${s}`).join('\n');
    
    // Вызовы
    const challenges = profile.challenges || ['Не указаны'];
    replacements['{{CHALLENGES_LIST}}'] = challenges.map(c => `• ${c}`).join('\n');
    
    // Адаптация под когнитивный стиль
    replacements['{{COGNITIVE_ADAPTATION}}'] = getCognitiveAdaptation(profile.cognitive_style);
    
    // Адаптация сложности
    replacements['{{DIFFICULTY_ADAPTATION}}'] = getDifficultyAdaptation(profile.current_level, profile.target_level, profile.learning_pace);
    replacements['{{INITIAL_DIFFICULTY}}'] = getInitialDifficulty(profile.current_level);
    
    // Стиль обратной связи
    replacements['{{FEEDBACK_STYLE}}'] = getFeedbackStyle(profile.feedback_preference);
    
    // Применяем все замены
    for (const [placeholder, value] of Object.entries(replacements)) {
        prompt = prompt.split(placeholder).join(value);
    }
    
    return prompt;
}

function getCognitiveStyleDescription(style) {
    const descriptions = {
        'визуальный': 'Визуальный (предпочитает схемы, диаграммы, видео)',
        'аудиальный': 'Аудиальный (предпочитает объяснения, подкасты, обсуждения)',
        'кинестетический': 'Кинестетический (предпочитает практику, эксперименты)',
        'комбинированный': 'Комбинированный (использует разные каналы восприятия)'
    };
    return descriptions[style] || style || 'комбинированный';
}

function getCognitiveAdaptation(style) {
    const adaptations = {
        'визуальный': `**Адаптация для визуала:**
- Используй ASCII-диаграммы, схемы, таблицы
- Структурируй информацию визуально (списки, иерархии)
- Предлагай рисовать mind-maps
- Минимизируй длинные текстовые блоки`,
        
        'аудиальный': `**Адаптация для аудиала:**
- Объясняй словами, как будто рассказываешь вслух
- Используй аналогии и метафоры
- Поощряй проговаривание вслух
- Предлагай обсуждать идеи`,
        
        'кинестетический': `**Адаптация для кинестетика:**
- Давай практические задания сразу
- Минимум теории — максимум действий
- "Попробуй сам, потом объясню почему"
- Используй реальные примеры из его жизни`,
        
        'комбинированный': `**Адаптация для комбинированного стиля:**
- Чередуй форматы: текст → схема → практика
- Адаптируйся к текущей теме
- Спрашивай, какой формат сейчас удобнее`
    };
    return adaptations[style] || adaptations['комбинированный'];
}

function getDifficultyAdaptation(current, target, pace) {
    const gap = (target || 8) - (current || 3);
    const paceMultiplier = pace === 'быстрый' ? 1.3 : pace === 'медленный' ? 0.7 : 1;
    
    if (gap <= 2) {
        return `**Небольшой разрыв (${gap} уровней):** Фокус на глубине и нюансах. Можно быстро переходить к продвинутым темам.`;
    } else if (gap <= 5) {
        return `**Средний разрыв (${gap} уровней):** Систематическое построение от основ к продвинутому. Регулярные проверки понимания.`;
    } else {
        return `**Большой разрыв (${gap} уровней):** Начни с фундамента. Не спеши. Убедись в крепкой базе перед усложнением.`;
    }
}

function getInitialDifficulty(currentLevel) {
    const level = parseInt(currentLevel) || 3;
    if (level <= 2) return 'Начальный (базовые концепции, много примеров)';
    if (level <= 5) return 'Средний (концепции + применение)';
    if (level <= 7) return 'Продвинутый (нюансы, edge cases)';
    return 'Экспертный (глубокая специализация)';
}

function getFeedbackStyle(preference) {
    const styles = {
        'мягкий': `**Стиль: Мягкий**
- Начинай с позитива
- Критику формулируй как "возможность улучшить"
- Используй "мы" вместо "ты"
- Много поддержки и поощрения
- Избегай резких формулировок`,
        
        'сбалансированный': `**Стиль: Сбалансированный**
- Честная оценка без приукрашивания
- Похвала за реальные достижения
- Прямое указание на ошибки
- Конструктивные предложения
- Уважительный тон`,
        
        'жесткий': `**Стиль: Жёсткий**
- Прямолинейность без смягчений
- "Это неверно, потому что..."
- Высокие стандарты
- Минимум похвалы — фокус на улучшении
- Никакого поддакивания`
    };
    return styles[preference] || styles['сбалансированный'];
}

// Показ результатов
function showResults(profile, personalizedPrompt) {
    // Скрываем шаги 1-2, показываем шаг 3
    document.getElementById('hw-step-1').style.display = 'none';
    document.getElementById('hw-step-2').style.display = 'none';
    document.getElementById('hw-step-3').style.display = 'block';
    
    // Обновляем прогресс
    document.getElementById('hw-progress-fill').style.width = '100%';
    document.getElementById('hw-current-step').textContent = '3';
    
    // Заполняем резюме профиля
    const summaryHtml = `
        <h4>👤 ВАШ ПЕДАГОГИЧЕСКИЙ ПРОФИЛЬ</h4>
        <div class="profile-grid">
            <div class="profile-item">
                <span class="profile-label">Область</span>
                <span class="profile-value">${profile.knowledge_area || '—'}</span>
            </div>
            <div class="profile-item">
                <span class="profile-label">Когнитивный стиль</span>
                <span class="profile-value">${profile.cognitive_style || '—'}</span>
            </div>
            <div class="profile-item">
                <span class="profile-label">Темп обучения</span>
                <span class="profile-value">${profile.learning_pace || '—'}</span>
            </div>
            <div class="profile-item">
                <span class="profile-label">Уровень</span>
                <span class="profile-value">${profile.current_level || '?'}/10 → ${profile.target_level || '?'}/10</span>
            </div>
            <div class="profile-item">
                <span class="profile-label">Обратная связь</span>
                <span class="profile-value">${profile.feedback_preference || '—'}</span>
            </div>
            <div class="profile-item">
                <span class="profile-label">Время/неделю</span>
                <span class="profile-value">${profile.available_hours_per_week || '?'} часов</span>
            </div>
        </div>
    `;
    document.getElementById('profile-summary').innerHTML = summaryHtml;
    
    // Заполняем рекомендации
    const recommendations = generateRecommendations(profile);
    const recsHtml = `
        <h4>💡 РЕКОМЕНДАЦИИ ДЛЯ ВАС</h4>
        <ul class="recommendations-list">
            ${recommendations.map(r => `<li>${r}</li>`).join('')}
        </ul>
    `;
    document.getElementById('profile-recommendations').innerHTML = recsHtml;
    
    // Заполняем промт
    document.getElementById('personalized-prompt').value = personalizedPrompt;
    
    // Скроллим к результату
    document.getElementById('hw-step-3').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function generateRecommendations(profile) {
    const recs = [];
    
    // По когнитивному стилю
    if (profile.cognitive_style === 'визуальный') {
        recs.push('Используйте диаграммы, схемы и визуализации');
    } else if (profile.cognitive_style === 'аудиальный') {
        recs.push('Проговаривайте материал вслух, обсуждайте идеи');
    } else if (profile.cognitive_style === 'кинестетический') {
        recs.push('Сразу переходите к практике, учитесь на действиях');
    }
    
    // По темпу
    if (profile.learning_pace === 'медленный') {
        recs.push('Делайте паузы для "переваривания" новых идей');
    } else if (profile.learning_pace === 'быстрый') {
        recs.push('Не бойтесь ускоряться, если чувствуете уверенность');
    }
    
    // По прокрастинации
    if (profile.procrastination_level === 'высокий' || profile.procrastination_level === 'средний') {
        recs.push('Разбивайте обучение на короткие сессии по 25-30 минут');
    }
    
    // По стрессу
    if (parseInt(profile.stress_level) >= 7) {
        recs.push('Начинайте с простых тем для снижения тревожности');
    }
    
    // По обратной связи
    if (profile.feedback_preference === 'жесткий') {
        recs.push('Ожидайте прямолинейной критики без смягчения');
    } else if (profile.feedback_preference === 'мягкий') {
        recs.push('Педагог будет поддерживать и мотивировать вас');
    }
    
    // Общие
    recs.push('Регулярно практикуйтесь: теория без практики не работает');
    
    return recs.slice(0, 5); // Максимум 5 рекомендаций
}

// Копирование персонализированного промта
window.copyPersonalizedPrompt = () => {
    const prompt = document.getElementById('personalized-prompt').value;
    navigator.clipboard.writeText(prompt).then(() => {
        showToast('✅ Промт скопирован! Вставьте в ChatGPT или Claude');
    }).catch(err => {
        const textarea = document.getElementById('personalized-prompt');
        textarea.select();
        document.execCommand('copy');
        showToast('✅ Промт скопирован!');
    });
};

// Сброс (начать заново)
window.resetHomework = () => {
    document.getElementById('hw-step-1').style.display = 'block';
    document.getElementById('hw-step-2').style.display = 'block';
    document.getElementById('hw-step-3').style.display = 'none';
    document.getElementById('profile-text').value = '';
    document.getElementById('upload-zone').classList.remove('file-loaded');
    document.getElementById('hw-progress-fill').style.width = '33%';
    document.getElementById('hw-current-step').textContent = '1';
    document.getElementById('homework').scrollIntoView({ behavior: 'smooth' });
};

// CSS для toast анимации (добавляем динамически)
const toastStyles = document.createElement('style');
toastStyles.textContent = `
@keyframes toastIn {
    from { opacity: 0; transform: translateX(-50%) translateY(20px); }
    to { opacity: 1; transform: translateX(-50%) translateY(0); }
}
@keyframes toastOut {
    from { opacity: 1; transform: translateX(-50%) translateY(0); }
    to { opacity: 0; transform: translateX(-50%) translateY(20px); }
}
`;
document.head.appendChild(toastStyles);
'''

# ============================================================
# ОБНОВЛЕНИЕ CONTENT.JSON
# ============================================================

def update_content_json(content_path):
    """Добавляем данные для блока homework в content.json"""
    try:
        with open(content_path, 'r', encoding='utf-8') as f:
            content = json.load(f)
    except FileNotFoundError:
        content = {}
    
    # Добавляем секцию homework
    content['homework'] = {
        "title": "🎯 ДОМАШНЕЕ ЗАДАНИЕ",
        "subtitle": "Получите персонального ИИ-педагога, настроенного именно под вас"
    }
    
    with open(content_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Обновлён {content_path}")


# ============================================================
# ГЛАВНАЯ ФУНКЦИЯ
# ============================================================

def main():
    print("=" * 60)
    print("НЕЙРО-ЮНИТ: Обновление v4.0")
    print("Блок 'Домашнее задание: Персональный ИИ педагог'")
    print("=" * 60)
    
    # Создаём директории если нужно
    os.makedirs(os.path.join(BASE_DIR, 'templates'), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, 'static/css'), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, 'static/js'), exist_ok=True)
    
    # Сохраняем HTML блок
    html_path = os.path.join(BASE_DIR, 'homework_block.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(HOMEWORK_HTML)
    print(f"✅ Создан {html_path}")
    
    # Сохраняем CSS
    css_path = os.path.join(BASE_DIR, 'homework_styles.css')
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(HOMEWORK_CSS)
    print(f"✅ Создан {css_path}")
    
    # Сохраняем JS
    js_path = os.path.join(BASE_DIR, 'homework_scripts.js')
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(HOMEWORK_JS)
    print(f"✅ Создан {js_path}")
    
    # Сохраняем промты отдельно для удобства
    profiling_path = os.path.join(BASE_DIR, 'prompts/profiling_prompt.md')
    os.makedirs(os.path.dirname(profiling_path), exist_ok=True)
    with open(profiling_path, 'w', encoding='utf-8') as f:
        f.write(PROFILING_PROMPT)
    print(f"✅ Создан {profiling_path}")
    
    tutor_path = os.path.join(BASE_DIR, 'prompts/personalized_tutor_template.md')
    with open(tutor_path, 'w', encoding='utf-8') as f:
        f.write(PERSONALIZED_TUTOR_TEMPLATE)
    print(f"✅ Создан {tutor_path}")
    
    print("\n" + "=" * 60)
    print("ИНСТРУКЦИИ ПО ИНТЕГРАЦИИ:")
    print("=" * 60)
    print("""
1. ДОБАВЬТЕ HTML БЛОК в index.html:
   - Найдите секцию <!-- GENERATOR SECTION -->
   - ПОСЛЕ неё (перед <!-- OFFER SECTION -->)
   - Вставьте содержимое homework_block.html

2. ДОБАВЬТЕ CSS СТИЛИ:
   - Откройте static/css/style.css
   - В конец файла добавьте содержимое homework_styles.css

3. ДОБАВЬТЕ JAVASCRIPT:
   - Откройте static/js/main.js
   - В конец файла (перед закрывающей скобкой DOMContentLoaded)
   - Добавьте содержимое homework_scripts.js

4. ПРОВЕРЬТЕ РАБОТУ:
   - Откройте сайт
   - Прокрутите до блока "Домашнее задание"
   - Проверьте копирование промта
   - Проверьте загрузку файла
   - Проверьте генерацию персонализированного промта

ГОТОВО! 🎉
""")

if __name__ == '__main__':
    main()
