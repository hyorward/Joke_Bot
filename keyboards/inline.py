from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_joke_button():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Анекдот дня 😂", callback_data="get_joke")]
        ]
    )
    return keyboard
