from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class class_inf:
    # 클래스 생성자 정의
    def __init__(self, name, professor, hour):
        self.name = name
        self.professor = professor
        self.hour = hour


# 과목 정보를 담는 리스트
subjects = []


def set_sub():
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
