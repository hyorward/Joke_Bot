from aiogram import Router
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from keyboards.inline import get_joke_button
from database import get_daily_joke, generate_voice_message
import os

router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Нажми кнопку, чтобы получить анекдот дня.", reply_markup=get_joke_button())

@router.callback_query(lambda c: c.data == "get_joke")
async def send_joke(callback: CallbackQuery):
    joke = get_daily_joke()  # Получаем анекдот дня

    # Отправляем анекдот в виде текста
    await callback.message.answer(f"😂 Анекдот дня:\n\n{joke}")

    # Генерируем голосовое сообщение и сохраняем путь к файлу
    audio_file = generate_voice_message(joke)

    # Проверяем, существует ли файл
    if not audio_file or not os.path.exists(audio_file):
        await callback.message.answer("Ошибка: голосовой файл не найден!")
        return

    # Отправляем голосовое сообщение
    await callback.message.answer_voice(FSInputFile(audio_file))
    await callback.answer()

    # Удаляем файл после отправки
    os.remove(audio_file)
