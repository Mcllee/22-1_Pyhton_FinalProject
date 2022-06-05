# 2022-1 Python Final Project

import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from selenium import webdriver
import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import pytz
import datetime
import schedule
from selenium.webdriver.common.by import By

import WebLogin as WL

token = '5374345704:AAGQzrf8WsaUbYhV-_R0pvqlH-F0arA3kEw'
id = 5312362183
bot = telegram.Bot(token)


def job():
    now = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
    days = ['월', '화', '수', '목', '금', '토', '일']
    weekday = days[datetime.date(now.year, now.month, now.day).weekday()]

    if weekday != '토' and weekday != '일':
        subs = WL.set_sub()
        subs = subs.split('\n')
        for sub in subs:
            sub = sub.split(' ')
            for s in sub[2::3]:
                if (int(s[0:2]) == now.hour) and (int(s[3:5]) == now.minute + 10) and sub[1] == weekday:
                    bot.send_message(chat_id=id,
                                     text='[수업 시간 10분 전 알림]\n과목: ' + sub[0] + '\n시간: ' + sub[2] + ' (' + sub[1] + ')')
                elif int(s[0:2]) == now.hour + 1 and int(s[3:5]) == now.minute - 50 and sub[1] == weekday:
                    bot.send_message(chat_id=id,
                                     text='[수업 시간 10분 전 알림]\n과목: ' + sub[0] + '\n시간: ' + sub[2] + ' (' + sub[1] + ')')
    if now.minute == 0:
        bot.send_message(chat_id=id, text=f"명철씌 정각 알람이에요!\n현재시각: {now.hour}:{now.minute} 입니다!")
    elif now.hour == 8 and now.minute == 30:
        now = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
        todo_list = f'완전 상쾌한 아침이야!!!\n오늘 부셔버릴 일들은 다음과 같아\n' + WL.get_todo_list()
        bot.send_message(chat_id=id, text=todo_list)
        bot.send_message(chat_id=id, text=WL.set_sub())


def handler(update, context):
    global schedule_loop

    user_text = update.message.text  # 사용자가 보낸 메세지를 user_text 변수에 저장합니다.
    if user_text =='종료':
        schedule_loop = False
        updater.stop()
        exit()
    elif user_text == '내일수업' or user_text == '내일 수업' or user_text == '내일':
        tomororow_sub = WL.tomorrow_sub()
        tomororow_sub = tomororow_sub.split(' ')
        sum_text = '[내일 수업 알림]\n\n'
        for name, week, hour in zip(tomororow_sub[::3], tomororow_sub[1::3], tomororow_sub[2::3]):
            sum_text += f'과목: {name}\n시간: {hour} ({week})\n\n'
        bot.send_message(chat_id=id,
                         text=sum_text)
    elif user_text == '일정':
        now = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
        todo_list = f'[{now.month}월 {now.day}일 해야할 일]\n' + WL.get_todo_list()
        bot.send_message(chat_id=id, text=todo_list)
    elif user_text == "수업":
        bot.send_message(chat_id=id, text=WL.set_sub())
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


schedule_loop = True
schedule.every(30).seconds.do(job)

# Updater
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
updater.start_polling()



while schedule_loop:
    echo_handler = MessageHandler(Filters.text, handler)
    dispatcher.add_handler(echo_handler)
    schedule.run_pending()
    time.sleep(1)
