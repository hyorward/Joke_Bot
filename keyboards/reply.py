from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_joke_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="😂 Получить анекдот")]],
        resize_keyboard=True  # Чтобы клавиатура была компактной
    )
    return keyboard
