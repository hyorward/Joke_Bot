from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_joke_button():
    button = InlineKeyboardButton(text="Получить случайный анекдот", callback_data="get_joke")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])  # Исправлено: передаем список кнопок
    return keyboard
