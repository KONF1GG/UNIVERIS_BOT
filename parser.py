from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import func
import sql as db
from private import config

class pars:

    def __init__(self):
        # задаем настройки нестандартного запуска (браузер работает даже после окончания работы python)
        o = Options()
        o.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=o)

    def get_authorization(self, log, pas):

        self.driver.get('https://studlk.susu.ru/Account/Login')

        login = self.driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div[1]/form/div/fieldset/div[1]/table/tbody/tr/td/input')
        login.send_keys(log)

        password = self.driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div[1]/form/div/fieldset/div[2]/table/tbody/tr/td/input')
        password.send_keys(pas)

        enter = self.driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div[1]/form/div/fieldset/table/tbody/tr[1]/td/div/div')
        enter.click()

    def enter_to_schedule(self):
        time.sleep(2)

        menu_educational_activity = self.driver.find_element(By.XPATH, '/html/body/div[4]/div/ul/li[2]/div[2]')
        menu_educational_activity.click()
        time.sleep(2)

        menu_schedule = self.driver.find_element(By.XPATH, '/html/body/div[4]/div/ul/li[2]/ul/li[1]/a')
        menu_schedule.click()
        time.sleep(3)

        menu = self.driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div')
        menu.click()

    def enter_to_start_of_semester(self):
        time.sleep(2)

        months = self.driver.find_element(By.XPATH, '/html/body/div[5]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr/td/table[2]/tbody/tr[1]/td/table/tbody/tr[1]/td/table/tbody/tr/td[5]/span')
        months.click()

        time.sleep(2)

        years = self.driver.find_element(By.XPATH, '/html/body/div[5]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr/td/table[2]/tbody/tr[1]/td/table/tbody/tr[1]/td/table/tbody/tr/td[5]/span')
        years.click()

        time.sleep(2)

        year_2022 = self.driver.find_element(By.ID, 'dateNavigator_cal_yc_3')
        year_2022.click()

        time.sleep(2)

        september = self.driver.find_element(By.ID, 'dateNavigator_cal_yc_8')
        september.click()

        time.sleep(2)

        first_day = self.driver.find_element(By.XPATH, '/html/body/div[5]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td[5]')
        first_day.click()

    def schedule_to_db(self, sql):
        # count_days = int(input('Введите количество дней которые нужно спарсить: '))

        def get_next_day():
            next_day = self.driver.find_element(By.XPATH, '//div[@title="Вперед"]')
            next_day.click()
            time.sleep(2)

        for i in range(270):
            print()
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            day_lessons = []
            date = soup.find(id="scheduler_containerBlock_horizontalContainer").text[4:][:-8]
            lessons = soup.find_all(style="margin-top: 5px; text-align: center; font: 8pt Tahoma; color: #37414D;")
            if len(lessons) != 0:
                for lesson in lessons:
                    day_lessons.append(lesson.text.strip())

                day_times = soup.find_all('label')
                time_list = []
                for time_ in day_times:
                    time_list.append(time_.text)

                lesson_schedule_dict = {}
                day_counter = 0
                time_counter = 0

                for lesson_part in day_lessons:
                    day_counter += 1
                    if day_counter == 1:
                        if func.string_is_digit(lesson_part.split()[-1]): # and lesson_part != 'Деловой иностранный язык'
                            lesson_schedule_dict['auditory'] = lesson_part.split()[-1]
                            lesson_schedule_dict['name'] = ' '.join(lesson_part.split()[:-1])
                        else:
                            lesson_schedule_dict['name'] = lesson_part
                            lesson_schedule_dict['auditory'] = '???'
                    elif day_counter == 2:
                        lesson_schedule_dict['type'] = lesson_part
                    elif day_counter == 3:
                        if lesson_schedule_dict['name'] == 'Деловой иностранный язык':
                            lesson_schedule_dict['teacher'] = 'Абудулрахман'
                        else:
                            lesson_schedule_dict['teacher'] = lesson_part
                        day_counter = 0
                        lesson_schedule_dict['time'] = time_list[time_counter]
                        lesson_schedule_dict['date'] = date
                        time_counter += 1

                        sql.insert_into(lesson_schedule_dict['time'],
                                        lesson_schedule_dict['name'],
                                        lesson_schedule_dict['auditory'],
                                        lesson_schedule_dict['teacher'],
                                        lesson_schedule_dict['date'],
                                        lesson_schedule_dict['type'])

                get_next_day()

            elif date.split(',')[0] == 'четверг':
                # print('военка')
                get_next_day()
            else:
                # print("пар нет!")
                get_next_day()