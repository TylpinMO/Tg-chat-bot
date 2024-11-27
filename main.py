import asyncio
import random
import json
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage

# Токен вашего бота
BOT_TOKEN = "8020924248:AAGYReHUfHc0C9sBlDf5sV2sWtem6jq_GXE"

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Статусы пользователей
STATUSES = [
    "Король Нахаловки", "Зам. короля", "Смотрящий", "Хоуми", 
    "Большой брат", "Младший брат", "Пупуня", 
    "Убежище", "Попуск", "Пять курица"
]

# Пути к файлу с данными
DATA_FILE = "homie_data.json"

# Функции для работы с базой данных
def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

# Обновление данных пользователя
def update_homie_points(user_id, username):
    data = load_data()
    user = data.get(str(user_id), {"username": username, "points": 0, "last_claim": None})
    now = datetime.now()

    # Проверка на ограничение в 6 часов
    if user["last_claim"]:
        last_claim_time = datetime.fromisoformat(user["last_claim"])
        if now - last_claim_time < timedelta(hours=6):
            return None

    # Выдача поинтов
    points = random.randint(1, 100)
    user["points"] += points
    user["last_claim"] = now.isoformat()
    user["username"] = username  # Обновляем имя пользователя
    data[str(user_id)] = user
    save_data(data)
    return user["points"], points

# Генерация статистики с количеством поинтов
def generate_stats():
    data = load_data()
    leaderboard = sorted(data.items(), key=lambda x: x[1]["points"], reverse=True)[:10]
    stats = ["Стата мужиков на районе:"]
    for index, (user_id, user_data) in enumerate(leaderboard, start=1):
        username = user_data["username"]
        status = STATUSES[index - 1] if index <= len(STATUSES) else "Новичок"
        points = user_data["points"]
        stats.append(f"{index}. {status} - @{username} - {points} карамелек")
    return "\n".join(stats)

# Хэндлер для команды /homie
@dp.message(F.text == "/homie@HomieHahBot")
async def homie_handler(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name

    result = update_homie_points(user_id, username)
    if result is None:
        await message.reply("Ты уже получал карамельки за последние 6 часов. Попробуй позже!")
    else:
        user_points, points_gained = result
        await message.reply(
            f"@{username}, ты получил {points_gained} карамелек. Всего у тебя {user_points} карамелек!"
        )

# Хэндлер для команды /statshomie
@dp.message(F.text == "/statshomie@HomieHahBot")
async def stats_handler(message: Message):
    stats_message = generate_stats()
    await message.reply(stats_message)

# Главная функция для запуска бота
async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())