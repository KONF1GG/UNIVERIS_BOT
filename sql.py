import sys
import MySQLdb
import datetime
import locale


class MySql:

    def __init__(self, host, user, password, db_name):
        try:
            self.connection = MySQLdb.connect(host, user, password, db_name)
        except MySQLdb.Error as e:
            print(f"Error connecting to MySQL Server: {e}")
            sys.exit(1)

        self.cursor = self.connection.cursor()

    def insert_into(self, time_, lesson, auditory, teacher, date, type_):
        try:
            self.cursor.execute(f"INSERT INTO `semester`(`time`, `lesson`, `auditory`, `teacher`, `date`, `type`) "
                            f"VALUES ('{time_}','{lesson}','{auditory}','{teacher}','{date}','{type_}')")
        except MySQLdb.Error as e:
            print(f'Error inserting into MySQL Server: {e}')

        self.connection.commit()

    def output_db(self):
        try:
            self.cursor.execute('SELECT * FROM `semester`')
            rows = self.cursor.fetchall()
            for row in rows:
                print(row)
                print()
        except MySQLdb.Error as e:
            print(f'Error selecting from MySQL Server: {e}')

    def delete_all_from_db(self):
        try:
            self.cursor.execute('DELETE FROM `semester`')
        except MySQLdb.Error as e:
            print(f'Error with deleting from MySQL: {e}')
        self.connection.commit()

    def get_day_schedule(self, date):
        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

        month_names = ['', 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября',
                       'октября', 'ноября', 'декабря']
        weekday_names = ['', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

        def format_date(date_string):
            date_obj = datetime.datetime.strptime(date_string, '%d.%m')
            formatted_date = weekday_names[date_obj.weekday()] + ', ' + str(date_obj.day) + ' ' + month_names[
                date_obj.month]

            return formatted_date.lower()

        formatted_date = format_date(date)

        query = f"SELECT time, lesson, auditory, type, teacher FROM semester WHERE date='{formatted_date}'"

        rows = []
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
        except MySQLdb.Error as e:
            print(f'Error with MySQL: {e}')
        self.connection.commit()

        rows_str = '\n\n'.join([' '.join(map(str, row)) for row in rows])
        if rows_str == '':
            return 'пар нет'
        return rows_str

    def get_exam_day(self, lesson_name):
        query = f"SELECT date FROM semester WHERE lesson='{lesson_name}' AND type='Экзамен'"

        try:
            self.cursor.execute(query)
            date = self.cursor.fetchall()
        except MySQLdb.Error as e:
            print(f'Error with MySQL: {e}')
            date = 'Ошибка получения даты'

        return date

    def get_consultation_day(self, lesson_name):
        query = f"SELECT date FROM semester WHERE lesson='{lesson_name}' AND type='Консультация к промежуточной аттестации'"

        try:
            self.cursor.execute(query)
            date = self.cursor.fetchall()
        except MySQLdb.Error as e:
            print(f'Error with MySQL: {e}')
            date = 'Ошибка получения даты'

        return date


    def get_remaining_lessons(self, lesson_name):
        # Словарь для преобразования названий месяцев на русском языке в их номера
        months_ru_to_en = {
            'января': '01',
            'февраля': '02',
            'марта': '03',
            'апреля': '04',
            'мая': '05',
            'июня': '06',
            'июля': '07',
            'августа': '08',
            'сентября': '09',
            'октября': '10',
            'ноября': '11',
            'декабря': '12'
        }

        query = f"SELECT date, type FROM semester WHERE lesson='{lesson_name}'"

        date_str_fetchall = ()
        try:
            self.cursor.execute(query)
            date_str_fetchall = self.cursor.fetchall()
        except MySQLdb.Error as e:
            print(f'Error with MySQL: {e}')
        self.connection.commit()

        today = datetime.date.today()
        count_practice = 0
        count_lecture = 0
        count_exam = 0
        count_consultation = 0
        for date_str in date_str_fetchall:
            # Разбиваем строку на слова и извлекаем нужные значения
            day, month_ru = date_str[0].split(', ')[1].split(' ')
            month_en = months_ru_to_en[month_ru]
            year = str(datetime.datetime.now().year)

            # Формируем объект datetime и выводим его в формате для SQL
            date_obj = datetime.datetime.strptime(f"{year}-{month_en}-{day}", '%Y-%m-%d')
            if today < date_obj.date():
                if date_str[1] == 'Практические занятия и семинары':
                    count_practice += 1
                elif date_str[1] == 'Лекции':
                    count_lecture += 1
                elif date_str[1] == 'Экзамен':
                    count_exam += 1
                elif date_str[1] == 'Консультация к промежуточной аттестации':
                    count_consultation += 1
        return count_lecture, count_practice, count_exam, count_consultation









