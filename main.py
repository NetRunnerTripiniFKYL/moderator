import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from dotenv import load_dotenv
load_dotenv()
import os

from handlers import user, admin, moderation 

async def main():
    # Инициализация бота и диспетчера
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher(storage=MemoryStorage())

    # Подключаем роутеры
    dp.include_router(user.router)
    dp.include_router(admin.router)
    dp.include_router(moderation.router)

    # Базовая реакция на ошибки (например, неизвестные команды)
    @dp.errors()
    async def on_error(event: Message, exception: Exception):
        print(f"[ERROR] {exception}")

    print("✅ Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())