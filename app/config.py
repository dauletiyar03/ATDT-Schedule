from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

# Токен бота
TOKEN_API = "7854463809:AAHxlVHfZNyvBDrcflQCHNRGyfEIovlmzBE"

# Создание бота, хранилища и диспетчера
bot = Bot(token=TOKEN_API)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
