from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime
import pytz


class class_inf:
    # 클래스 생성자 정의
    def __init__(self, name, professor, hour):
        self.name = name
        self.professor = professor
        self.hour = hour


# 과목 정보를 담는 리스트
subjects = []


def set_sub():
    subjects.clear()

    driver = webdriver.Chrome()
    driver.get('http://eclass.tukorea.ac.kr/ilos/main/member/login_form.acl')
    driver.find_element(By.XPATH, '//*[@id="usr_id"]').click()
    driver.find_element(By.XPATH, '//*[@id="usr_id"]').send_keys('2018184020')
    driver.find_element(By.XPATH, '//*[@id="usr_pwd"]').click()
    driver.find_element(By.XPATH, '//*[@id="usr_pwd"]').send_keys('1077111')
    driver.find_element(By.XPATH, '//*[@id="login_btn"]').click()
    driver.find_element(By.XPATH, '//*[@id="quick-menu-index"]/a[1]/div/img').click()

    time.sleep(1)
    elms = driver.find_element(By.XPATH, '//*[@id="lecture_list"]/div[1]/div[1]').text
    driver.close()

    elms = elms.split('\n')

    for name, professor, hour in zip(elms[1::3], elms[2::3], elms[3::3]):
        subjects.append(class_inf(name, professor, hour))

    now = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
    days = ['월', '화', '수', '목', '금', '토', '일']
    today = days[datetime.date(now.year, now.month, now.day).weekday()]

    todo_list = ''

    for line in subjects:
        line.hour = line.hour.split(' ')
        if line.hour[0] == today:
            todo_list += (line.name + ' ' + line.hour[0] + ' ' + line.hour[2] + '\n')
        elif len(line.hour[3]) == 1 and line.hour[3] == today:
            todo_list += (line.name + ' ' + line.hour[3] + ' ' + line.hour[5] + '\n')
        elif today == '토' or today == '일':
            todo_list = f"야호! 오늘은 {today}요일!"
            break
    return todo_list


def tomorrow_sub():
    subjects.clear()

    driver = webdriver.Chrome()
    driver.get('http://eclass.tukorea.ac.kr/ilos/main/member/login_form.acl')
    driver.find_element(By.XPATH, '//*[@id="usr_id"]').click()
    driver.find_element(By.XPATH, '//*[@id="usr_id"]').send_keys('2018184020')
    driver.find_element(By.XPATH, '//*[@id="usr_pwd"]').click()
    driver.find_element(By.XPATH, '//*[@id="usr_pwd"]').send_keys('1077111')
    driver.find_element(By.XPATH, '//*[@id="login_btn"]').click()
    driver.find_element(By.XPATH, '//*[@id="quick-menu-index"]/a[1]/div/img').click()

    time.sleep(1)
    elms = driver.find_element(By.XPATH, '//*[@id="lecture_list"]/div[1]/div[1]').text
    driver.close()

    elms = elms.split('\n')

    for name, professor, hour in zip(elms[1::3], elms[2::3], elms[3::3]):
        subjects.append(class_inf(name, professor, hour))

    now = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
    days = ['화', '수', '목', '금', '토', '일', '월']
    today = days[datetime.date(now.year, now.month, now.day).weekday()]

    todo_list = ''

    for line in subjects:
        line.hour = line.hour.split(' ')
        if line.hour[0] == today:
            todo_list += (line.name + ' ' + line.hour[0] + ' ' + line.hour[2] + ' ')
        elif len(line.hour[3]) == 1 and line.hour[3] == today:
            todo_list += (line.name + ' ' + line.hour[3] + ' ' + line.hour[5] + ' ')
        elif today == '토' or today == '일':
            todo_list = f"야호! 오늘은 {today}요일!"
            break
    return todo_list


def get_todo_list():
    driver = webdriver.Chrome()
    driver.get('http://eclass.tukorea.ac.kr/ilos/main/member/login_form.acl')
    driver.find_element(By.XPATH, '//*[@id="usr_id"]').click()
    driver.find_element(By.XPATH, '//*[@id="usr_id"]').send_keys('2018184020')
    driver.find_element(By.XPATH, '//*[@id="usr_pwd"]').click()
    driver.find_element(By.XPATH, '//*[@id="usr_pwd"]').send_keys('1077111')
    driver.find_element(By.XPATH, '//*[@id="login_btn"]').click()
    driver.find_element(By.XPATH, '//*[@id="header"]/div[4]/div/fieldset/div/div[2]/img').click()

    time.sleep(1)
    elms = driver.find_element(By.CSS_SELECTOR, '#todo_list').text
    driver.close()

    return elms.replace('[', '\n[')
