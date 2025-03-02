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

    # Создание таблицы для хранения информации о дате последнего изменения анекдота
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

def get_random_joke():
    """Возвращает случайный анекдот из базы данных."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Выбираем случайный анекдот
    cursor.execute("SELECT text FROM jokes ORDER BY RANDOM() LIMIT 1")
    joke = cursor.fetchone()

    conn.close()
    return joke[0] if joke else "Извините, анекдоты закончились."

def generate_voice_message(joke_text):
    """Генерирует голосовое сообщение и сохраняет его в аудиофайл."""
    tts = gTTS(text=joke_text, lang='ru')
    audio_file = os.path.join(AUDIO_DIR, 'joke.mp3')
    tts.save(audio_file)
    return audio_file
