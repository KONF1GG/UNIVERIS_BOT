import sql as bd
import telebot
from telebot import types
from datetime import datetime, timedelta
import re
from private import authorization, config

class BOT:
    def __init__(self, token, classes):
        self.bot = telebot.TeleBot(token)
        self.classes = classes

    def start(self, message):
        self.bot.send_message(message.chat.id, '<b>Привет!</b>', parse_mode='html')

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        count_remaining = types.KeyboardButton('Осталось пар')
        tomorrow_schedule = types.KeyboardButton('Завтра')
        today_schedule = types.KeyboardButton('Сегодня')

        markup.add(count_remaining, tomorrow_schedule, today_schedule)
        self.bot.send_message(message.chat.id, 'Выберете дейстиве или напишите дату, например 22.05', reply_markup=markup)

    def generate_classes_markup(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        for class_name in self.classes:
            button = types.KeyboardButton(class_name)
            markup.add(button)

        return markup

    def handle_message(self, message):
        subject = False
        pattern = r'^\d{2}.\d{2}$'
        pattern2 = r'^\d{1}.\d{2}$'

        if message.text in self.classes:
            subject = True

        if re.match(pattern, message.text) or re.match(pattern2, message.text):
            sql = bd.MySql(config.host, config.user, config.password, config.db_name)

            try:
                self.bot.send_message(message.chat.id, f'{sql.get_day_schedule(message.text)}', parse_mode='html')
            except ValueError as e:
                self.bot.send_message(message.chat.id, f"Некорректно введена дата")

            sql.connection.close()

        elif message.text == 'Осталось пар':
            markup = self.generate_classes_markup()
            back_button = types.KeyboardButton('Назад')
            markup.add(back_button)

            self.bot.send_message(message.chat.id, 'Выберите предмет:', reply_markup=markup)

        elif subject:
            sql = bd.MySql(config.host, config.user, config.password, config.db_name)
            lecture, practice, exam, consultation = sql.get_remaining_lessons(message.text)
            sql.connection.close()

            bot_response = f'Количество оставшихся практик = {practice}\nКоличество оставшихся лекций = {lecture}'

            if consultation != 0 and exam == 0:
                sql = bd.MySql(config.host, config.user, config.password, config.db_name)
                date = sql.get_consultation_day(message.text)[0][0]
                sql.connection.close()
                bot_response += f'\nКонсультация: {date}'
            elif consultation == 0 and exam != 0:
                sql = bd.MySql(config.host, config.user, config.password, config.db_name)
                date = sql.get_exam_day(message.text)[0][0]
                sql.connection.close()
                bot_response += f'\nЭкзамен: {date}'
            elif consultation != 0 and exam != 0:
                sql = bd.MySql(config.host, config.user, config.password, config.db_name)
                date_ex = sql.get_exam_day(message.text)[0][0]
                date_cons = sql.get_consultation_day(message.text)[0][0]
                sql.connection.close()
                bot_response += f'\nКонсультация: {date_cons}\nЭкзамен: {date_ex}'

            self.bot.send_message(message.chat.id, bot_response)

        elif message.text == 'Назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            count_remaining = types.KeyboardButton('Осталось пар')
            tomorrow_schedule = types.KeyboardButton('Завтра')
            today_schedule = types.KeyboardButton('Сегодня')
            markup.add(count_remaining, tomorrow_schedule, today_schedule)
            self.bot.send_message(message.chat.id, 'Выберете дейстиве или например дату в формате 22.05', reply_markup=markup)

        elif message.text == 'Завтра':
            tomorrow = datetime.today() + timedelta(days=1)
            formatted_tomorrow = tomorrow.strftime('%d.%m')
            sql = bd.MySql(config.host, config.user, config.password, config.db_name)

            try:
                self.bot.send_message(message.chat.id, f'{sql.get_day_schedule(formatted_tomorrow)}', parse_mode='html')
            except ValueError as e:
                self.bot.send_message(message.chat.id, f"Некорректно введена дата")
                sql.connection.close()

        elif message.text == 'Сегодня':
            today = datetime.today()
            formatted_today = today.strftime('%d.%m')
            sql = bd.MySql(config.host, config.user, config.password, config.db_name)

            try:
                self.bot.send_message(message.chat.id, f'{sql.get_day_schedule(formatted_today)}', parse_mode='html')
            except ValueError as e:
                self.bot.send_message(message.chat.id, f"Некорректно введена дата")

            sql.connection.close()

        else:
            self.bot.send_message(message.chat.id, '<b>Я тебя не понимаю(</b>', parse_mode='html')

    def run(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.start(message)

        @self.bot.message_handler(content_types=['text'])
        def handle_message(message):
            self.handle_message(message)

        self.bot.polling(none_stop=True)

classes = ['Электроника', 'Деловой иностранный язык', 'Теория вероятностей и математическая статистика',
           'Безопасность сетей электронных вычислительных машин', 'Математическая логика и теория алгоритмов',
           'Физическая культура и спорт', 'Дискретная математика', 'Технологии и методы программирования',
           'Машинное обучение и анализ данных']

bot = BOT('5817689317:AAGETTdh7BC0X8E0Ox7Yer9EWVZ5hXUIRVE', classes)
