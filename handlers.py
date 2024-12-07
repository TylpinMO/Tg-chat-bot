import requests
import random

from datetime import datetime, timedelta
from utils.storage import get_user_data, update_user_data
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters
from utils.horoscope_data import get_horoscope
from config import WEATHER_API_KEY

# Состояние для ввода знака зодиака
ASK_SIGN = 1

# Обработчик команды /points
async def points(update, context):
  user_id = update.effective_user.id
  user_data = get_user_data(user_id)
  
  last_points_time = user_data.get("last_points")
  now = datetime.now()
  
  if last_points_time:
    last_points_time = datetime.fromisoformat(last_points_time)
    if now - last_points_time < timedelta(hours=6):
      remaining_time = timedelta(hours=6) - (now - last_points_time)
      hours, remainder = divmod(remaining_time.seconds, 3600)
      minutes, _ = divmod(remainder, 60)
      await update.message.reply_text(
        f"Вы уже получали тубрики. Следующие можно будет получить через {hours} ч. {minutes} мин."
      )
      return

  # Генерация случайного количества тубриков
  earned_points = random.randint(1, 100)
  new_balance = user_data["balance"] + earned_points
  update_user_data(user_id, balance=new_balance, last_points=now.isoformat())

  await update.message.reply_text(
    f"Вы получили {earned_points} тубриков! Ваш текущий баланс: {new_balance} тубриков."
  )

# Обработчик команды /horoscope
async def horoscope(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text("Введите ваш знак зодиака (например: Овен, Телец, Близнецы):")
  return ASK_SIGN

# Обработчик ввода знака зодиака
async def get_sign(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_sign = update.message.text.capitalize()
  horoscope_text = get_horoscope(user_sign)
  await update.message.reply_text(horoscope_text)
  return ConversationHandler.END

# Команда /weatherMOS
async def weather_mos(update, context):
  city = "Moscow"
  url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ru&appid={WEATHER_API_KEY}"
  
  try:
    response = requests.get(url)
    data = response.json()
    
    if data["cod"] == 200:
      city_name = data["name"]
      temp = data["main"]["temp"]
      weather = data["weather"][0]["description"]
      
      message = (
        f"Погода в {city_name}:\n"
        f"🌡 Температура: {temp}°C\n"
        f"🌥 Описание: {weather.capitalize()}"
      )
    else:
      message = f"Не удалось получить данные о погоде для {city}. Проверьте название города."
  except Exception as e:
    message = "Ошибка при запросе погоды. Попробуйте позже."
    print(f"Ошибка: {e}")
    
  await update.message.reply_text(message)

# Команда /weatherROS
async def weather_ros(update, context):
  city = "Rostov-on-Don"
  url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ru&appid={WEATHER_API_KEY}"
  
  try:
    response = requests.get(url)
    data = response.json()
    
    if data["cod"] == 200:
      city_name = data["name"]
      temp = data["main"]["temp"]
      weather = data["weather"][0]["description"]
      
      message = (
        f"Погода в {city_name}:\n"
        f"🌡 Температура: {temp}°C\n"
        f"🌥 Описание: {weather.capitalize()}"
      )
    else:
      message = f"Не удалось получить данные о погоде для {city}. Проверьте название города."
  except Exception as e:
    message = "Ошибка при запросе погоды. Попробуйте позже."
    print(f"Ошибка: {e}")
    
  await update.message.reply_text(message)

# Команда /happyny
async def happyny(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now()
    new_year = datetime(year=now.year + 1, month=1, day=1)
    remaining_time = new_year - now
    days = remaining_time.days
    hours, remainder = divmod(remaining_time.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    message = (
        f"До Нового года осталось {days}д:{hours}ч:{minutes}м. "
        f"Пора думать, как будем тусить! 🎉"
    )
    await update.message.reply_text(message)