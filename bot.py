import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import register_handlers
from utils import initialize_data

BOT_TOKEN = "7892546134:AAGeo2K5sdDlzIc9pb7SWEL6InjtVry7GsI"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

async def main():
    initialize_data()
    register_handlers(dp)
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())