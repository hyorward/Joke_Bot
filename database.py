import sqlite3
import os
import random
from datetime import datetime
from gtts import gTTS

DB_NAME = "jokes.db"
JOKES_FILE = "jokes.txt"
AUDIO_DIR = "audio_files"

# Создание директории для хранения аудиофайлов
if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)

def setup_database():
    """Создает таблицу и загружает анекдоты из файла, если их нет."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Создание таблицы для анекдотов, если ее нет
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jokes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        )
    ''')

    # Создание таблицы для хранения информации о дате изменения анекдота
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS joke_day (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            last_joke_id INTEGER,
            last_change_date TEXT
        )
    ''')

    # Проверка, если анекдоты еще не добавлены в базу
    cursor.execute("SELECT COUNT(*) FROM jokes")
    count = cursor.fetchone()[0]

    if count == 0 and os.path.exists(JOKES_FILE):
        with open(JOKES_FILE, "r", encoding="utf-8") as f:
            jokes = [line.strip() for line in f if line.strip()]
        
        cursor.executemany("INSERT INTO jokes (text) VALUES (?)", [(joke,) for joke in jokes])
        conn.commit()

    # Проверка, если запись с датой последнего изменения анекдота еще не существует
    cursor.execute("SELECT COUNT(*) FROM joke_day")
    count_day = cursor.fetchone()[0]

    if count_day == 0:
        cursor.execute("INSERT INTO joke_day (last_joke_id, last_change_date) VALUES (?, ?)", (1, datetime.now().strftime('%Y-%m-%d')))
        conn.commit()

    conn.close()

def get_daily_joke():
    """Возвращает анекдот дня и обновляет его, если дата изменилась."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT last_joke_id, last_change_date FROM joke_day")
    last_joke_id, last_change_date = cursor.fetchone()

    today = datetime.now().strftime('%Y-%m-%d')

    # Если дата изменилась, выбираем новый анекдот
    if last_change_date != today:
        new_joke_id = random.randint(1, 100)  # Или просто выбираем случайный ID
        cursor.execute("UPDATE joke_day SET last_joke_id = ?, last_change_date = ?", (new_joke_id, today))
        conn.commit()
        last_joke_id = new_joke_id

    # Получаем текст анекдота для текущего дня
    cursor.execute("SELECT text FROM jokes WHERE id = ?", (last_joke_id,))
    joke = cursor.fetchone()

    conn.close()
    return joke[0] if joke else "Анекдотов пока нет!"

def generate_voice_message(joke_text):
    """Генерирует голосовое сообщение и сохраняет его в аудиофайл."""
    tts = gTTS(text=joke_text, lang='ru')
    audio_file = os.path.join(AUDIO_DIR, 'joke.mp3')
    tts.save(audio_file)
    return audio_file
