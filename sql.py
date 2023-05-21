import sys
import MySQLdb
from datetime import datetime
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
            date_obj = datetime.strptime(date_string, '%d.%m')
            formatted_date = weekday_names[date_obj.weekday()] + ', ' + str(date_obj.day) + ' ' + month_names[
                date_obj.month]

            return formatted_date.capitalize()

        formatted_date = format_date(date)

        query = f"SELECT * FROM semester WHERE date = '{formatted_date}'"
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
        except MySQLdb.Error as e:
            print(f'Error with deleting from MySQL: {e}')
        self.connection.commit()

        rows_str = '\n'.join([', '.join(map(str, row)) for row in rows])
        return rows_str




