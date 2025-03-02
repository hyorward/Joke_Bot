from aiogram import Router
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from keyboards.reply import get_joke_reply_keyboard  # Импортируем Reply-клавиатуру
from database import get_random_joke, generate_voice_message
import os

router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    """Обработчик команды /start. Показывает приветственное сообщение и клавиатуру."""
    await message.answer(
        "Привет! Нажми кнопку, чтобы получить случайный анекдот.",
        reply_markup=get_joke_reply_keyboard()  # Используем Reply-клавиатуру
    )

@router.message(lambda message: message.text == "😂 Получить анекдот")  # Добавляем обработку кнопки
async def send_joke(message: Message):
    """Отправляет случайный анекдот в текстовом и голосовом формате."""
    joke = get_random_joke()
    
    await message.answer(f"😂 Анекдот:\n\n{joke}")

    # Генерируем голосовое сообщение
    audio_file = generate_voice_message(joke)

    if not audio_file or not os.path.exists(audio_file):
        await message.answer("Ошибка: голосовой файл не найден!")
        return

    await message.answer_voice(FSInputFile(audio_file))
