import logging

from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters
from config import BOT_TOKEN
from handlers import happyny, weather_ros, weather_mos, horoscope, get_sign, ASK_SIGN, points

logging.basicConfig(
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
  level=logging.INFO
)

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Регистрируем обработчики
    app.add_handler(CommandHandler("happyNY", happyny)) # До НГ осталось
    app.add_handler(CommandHandler("weatherROS", weather_ros)) # Погода в Ростове
    app.add_handler(CommandHandler("weatherMOS", weather_mos)) # Погода в Москве
    app.add_handler(CommandHandler("points", points)) # Получение тубриков
    
    # Обработчик для /horoscope
    horoscope_handler = ConversationHandler(
      entry_points=[CommandHandler("horoscope", horoscope)],
      states={
        ASK_SIGN: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_sign)],
      },
      fallbacks=[],
    )
    app.add_handler(horoscope_handler)
    
    #  Логируем старт бота
    logging.info("Бот успешно запущен и готов к работе!")

    # Запускаем бота
    app.run_polling()

if __name__ == "__main__":
    main()