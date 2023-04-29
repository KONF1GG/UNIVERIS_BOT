import sys
import MySQLdb


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


