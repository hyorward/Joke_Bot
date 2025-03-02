import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TOKEN
from database import setup_database
from handlers import joke

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    
    dp.include_router(joke.router)

    setup_database()  # Создаем базу данных при старте

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
