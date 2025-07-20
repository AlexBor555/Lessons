import telebot
from telebot import types
import config
import sqlite3
import re
import random  # Добавляем модуль random

# Инициализация бота
bot = telebot.TeleBot(config.BOT_TOKEN)

# --- Смайлики для настроения ---
HAPPY_EMOJIS = ["😄", "😊", "🥳", "😎", "👍"]
SAD_EMOJIS = ["😔", "😟", "😕", "🤔"]
EDIT_EMOJIS = ["✏️", "📝", "✍️"]
ADD_EMOJIS = ["➕", "✨", "🌟"]
DAY_EMOJIS = ["☀️", "🌤️", "🌥️", "🌦️", "🌧️", "🌨️", "🌈"]  # Для дней недели

# --- Глобальные переменные ---
admin_mode = False
editing_day = None
editing_lesson_index = None
current_user_id = None
lesson_to_delete_id = None
current_schedule = {}
editing_lesson_id = None
edit_state = None

# --- Инициализация базы данных ---
def create_database():
    conn = sqlite3.connect('schedule.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT NOT NULL,
            lesson TEXT NOT NULL,
            time TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_database()

# --- Функции для работы с базой данных ---
def get_schedule_from_db():
    conn = sqlite3.connect('schedule.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, day, lesson, time FROM schedule")
    schedule_data = cursor.fetchall()
    conn.close()

    schedule = {}
    for lesson_id, day, lesson, time in schedule_data:
        if day not in schedule:
            schedule[day] = []
        schedule[day].append({"id": lesson_id, "lesson": lesson, "time": time})
    return schedule

def add_lesson_to_db(day, lesson, time):
    conn = sqlite3.connect('schedule.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO schedule (day, lesson, time) VALUES (?, ?, ?)", (day, lesson, time))
    conn.commit()
    conn.close()

def update_lesson_in_db(lesson_id, day, lesson_name, lesson_time):
    conn = sqlite3.connect('schedule.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE schedule SET day = ?, lesson = ?, time = ? WHERE id = ?", (day, lesson_name, lesson_time, lesson_id))
    conn.commit()
