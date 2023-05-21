import sql as bd
import telebot
from private import authorization, config

bot = telebot.TeleBot('5817689317:AAGETTdh7BC0X8E0Ox7Yer9EWVZ5hXUIRVE')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '<b>Привет!</b>', parse_mode='html')

@bot.message_handler()
def get_day(message):
    sql = bd.MySql(config.host, config.user, config.password, config.db_name)
    bot.send_message(message.chat.id, f'{sql.get_day_schedule(message.text)}', parse_mode='html')
    sql.connection.close()

bot.polling(none_stop=True)

