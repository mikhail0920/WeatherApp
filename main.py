from exceptions import WeatherAPIError
from weather_api import get_weather

from telebot import TeleBot
from telebot.types import Message
from telebot.apihelper import ApiTelegramException
import os

API_KEY_TELEGRAM = os.environ['API_KEY_TELEGRAM']
bot = TeleBot(API_KEY_TELEGRAM)

@bot.message_handler(commands=['start'])
def handle_start( message: Message ) -> None:
    bot.reply_to( message, 'Привет! Дай мне название города и я определю в нём погоду! Мне мама с детства говорила, что я особенный :)' )

@bot.message_handler(content_types=['text'])
def handle_message( message: Message ) -> None:
    try:
        weather = get_weather( message.text )
        bot.reply_to( message, str(weather) )
    except WeatherAPIError:
        bot.reply_to(message, 'Извините, что-то пошло не так или вы ввели название несуществующего города, попробуйте еще раз ;)')
    except ApiTelegramException:
        print('Telegram Error!')
        exit(1)

bot.polling(none_stop=True)
