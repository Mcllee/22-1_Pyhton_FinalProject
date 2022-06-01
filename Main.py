# 2022-1 Python Final Project

import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from selenium import webdriver
import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

token = '5374345704:AAGQzrf8WsaUbYhV-_R0pvqlH-F0arA3kEw'
id = 5312362183
bot = telegram.Bot(token)

import pytz
import datetime
import schedule


def job():
    now = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
    if now.minute == 0:
        bot.send_message(chat_id=id, text=f"명철씌 정각 알람이에요!\n현재시각: {now.hour}:{now.minute} 입니다!")


schedule.every(1).minutes.do(job)


# Updater
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
updater.start_polling()


def handler(update, context):
    user_text = update.message.text  # 사용자가 보낸 메세지를 user_text 변수에 저장합니다.
    if user_text == '일정':
        pass
    elif user_text == "식당" or user_text == "밥" or user_text == "학식" or user_text == "ㅅㄷ" or user_text == "ㅂ" or user_text == "ㅎㅅ":

        bot.send_message(chat_id=id, text="이번주 식단입니다.")

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
        time.sleep(1)  # 스크린샹을 위해 잠시 멈춤(쉡 로딩)
        driver01.get_screenshot_as_file('screenshot01.png')

        driver02.get('https://ibook.kpu.ac.kr/Viewer/menu02')
        time.sleep(1)  # 스크린샹을 위해 잠시 멈춤(쉡 로딩)
        driver02.get_screenshot_as_file('screenshot02.png')

        driver01.close()
        driver02.close()

        bot.send_photo(chat_id=id, photo=open('screenshot01.png', 'rb'))
        bot.send_photo(chat_id=id, photo=open('screenshot02.png', 'rb'))
        os.remove('./screenshot01.png')
        os.remove('./screenshot02.png')
    else:
        try:
            bot.send_message(chat_id=id, text=eval(user_text))
        except:
            bot.send_message(chat_id=id, text="잘못된 명령어 입니다!")


echo_handler = MessageHandler(Filters.text, handler)
dispatcher.add_handler(echo_handler)

while True:
    schedule.run_pending()
    time.sleep(1)
