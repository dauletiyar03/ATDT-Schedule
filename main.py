import asyncio
import logging

from aiogram import Bot, Dispatcher
from app.config import TOKEN_API
from app.handlers import router, set_bot_commands

#Создаем бота и маршрутизатор
bot = Bot(token=TOKEN_API)
dp = Dispatcher()

async def main():
    dp.include_router(router)

    # Устанавливаем команды
    await set_bot_commands(bot)
    # Запускаем бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Инициализируем базу данных
    # initialize_database()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
