from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime
import pytz
from selenium.webdriver.chrome.service import Service
import os


class class_inf:
    # 클래스 생성자 정의
    def __init__(self, name, professor, hour):
        self.name = name
        self.professor = professor
        self.hour = hour


# 웹 스크랩 정보를 담는 str
elms = ''
# 과목 정보를 담는 리스트
subjects = []


def first_setting():
    global elms

    driver = webdriver.Chrome()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

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


def set_sub():
    subjects.clear()
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


def restaurant():
    now = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
    days = ['월', '화', '수', '목', '금', '토', '일']
    today = days[datetime.date(now.year, now.month, now.day).weekday()]

    if today == '월' and now.hour == 10:
        os.remove('./screenshot01.png')
        os.remove('./screenshot02.png')

    try:
        open('screenshot01.png').close()
        open('screenshot02.png').close()
    except:
        chrome_options01 = webdriver.ChromeOptions()
        chrome_options02 = webdriver.ChromeOptions()
        chrome_options01.add_argument("--headless")
        chrome_options01.add_argument("--no-sandbox")
        chrome_options01.add_argument("--disable-dev-shm-usage")
        chrome_options02.add_argument("--headless")
        chrome_options02.add_argument("--no-sandbox")
        chrome_options02.add_argument("--disable-dev-shm-usage")

        # chromedriver 위치 주의!
        driver01 = webdriver.Chrome(service=Service("chromedriver"), options=chrome_options01)
        driver02 = webdriver.Chrome(service=Service("chromedriver"), options=chrome_options02)

        driver01.get('https://ibook.kpu.ac.kr/Viewer/menu01')
        time.sleep(1)  # 스크린샹을 위해 잠시 멈춤(웹 로딩)
        driver01.get_screenshot_as_file('screenshot01.png')

        driver02.get('https://ibook.kpu.ac.kr/Viewer/menu02')
        time.sleep(1)  # 스크린샹을 위해 잠시 멈춤(웹 로딩)
        driver02.get_screenshot_as_file('screenshot02.png')

        driver01.close()
        driver02.close()

