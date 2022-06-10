import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
import time

import pytz
import datetime
import schedule

import WebLogin as WL

token = '5374345704:AAGQzrf8WsaUbYhV-_R0pvqlH-F0arA3kEw'
id = 5312362183
bot = telegram.Bot(token)
WL.first_setting()


def job():
    now = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
    days = ['월', '화', '수', '목', '금', '토', '일']
    weekday = days[datetime.date(now.year, now.month, now.day).weekday()]

    # 매번 갱신해 줄 정보들
    if weekday == '월' and now.hour < 11:
        WL.restaurant(True)  # 식당 정보를 월요일 갱신

    if weekday != '토' and weekday != '일':
        subs = WL.set_sub().split(' ')
        for name, day, h in zip(subs[::3], subs[1::3], subs[2::3]):
            if (int(h[0:2]) == now.hour) and (int(h[3:5]) == now.minute + 10) and weekday == day:
                bot.send_message(chat_id=id,
                                 text=f'[수업 시간 10분 전 알림]\n과목: ' + name + '\n시간: ' + h + ' (' + day + ')')
            elif (int(h[0:2]) == now.hour + 1) and (int(h[3:5]) == now.minute - 50) and weekday == day:
                bot.send_message(chat_id=id,
                                 text=f'[수업 시간 10분 전 알림]\n과목: ' + name + '\n시간: ' + h + ' (' + day + ')')
    if now.minute == 0:
        bot.send_message(chat_id=id, text=f"명철씌 정각 알람이에요!\n현재시각: {now.hour}:{now.minute} 입니다!")
        WL.weather(True)
    elif now.hour == 8 and now.minute == 30:
        now = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
        todo_list = f'완전 상쾌한 아침이야!!!\n오늘 부셔버릴 일들은 다음과 같아\n' + WL.get_todo_list()
        bot.send_message(chat_id=id, text=todo_list)
        bot.send_message(chat_id=id, text=WL.set_sub())
        WL.weather(False)
        bot.send_message(chat_id=id, text=f'오늘의 아침 날씨')
        bot.send_photo(chat_id=id, photo=open('weather02.png', 'rb'))


def handler(update, context):
    user_text = update.message.text  # 사용자가 보낸 메세지를 user_text 변수에 저장합니다.
    if user_text == '도움말' or user_text == '명령어' or user_text == '설명':
        order_list = '1. 내일 수업:    내일 시간표를 알려드려요!\n' \
                     '2. 일정:        오늘의 수업 시간표를 알려드려요!\n' \
                     '3. 수업:        e-Class에서 해야할 일들을 알려드려요!\n' \
                     '4. 식당:        팁 지하/E동 1층 식당의 메뉴를 알려드려요!'
        bot.send_message(chat_id=id, text=order_list)

    elif user_text == '내일수업' or user_text == '내일 수업' or user_text == '내일':
        tomororow_sub = WL.tomorrow_sub().split(' ')
        sum_text = '[내일 수업 알림]\n\n'
        for name, week, hour in zip(tomororow_sub[::3], tomororow_sub[1::3], tomororow_sub[2::3]):
            if hour[0] == '토' or hour[0] == '일':
                sum_text += f'오늘은 {hour[0]}요일!'
                break
            else:
                sum_text += f'과목: {name}\n시간: {hour} ({week})\n\n'
        bot.send_message(chat_id=id, text=sum_text)

    elif user_text == '일정':
        now = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
        todo_list = f'[{now.month}월 {now.day}일 해야할 일]\n' + WL.get_todo_list()
        bot.send_message(chat_id=id, text=todo_list)

    elif user_text == "수업" or user_text == "오늘":
        today_sub = WL.set_sub().split(' ')
        sum_text = '[오늘의 수업 안내!]\n\n'
        for name, week, hour in zip(today_sub[::3], today_sub[1::3], today_sub[2::3]):
            if hour[0] == '토' or hour[0] == '일':
                sum_text += f'오늘은 {hour[0]}요일!'
                break
            else:
                sum_text += f'과목: {name}\n시간: {hour} ({week})\n\n'
        bot.send_message(chat_id=id, text=sum_text)
        
    elif user_text == "날씨":
        now = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
        bot.send_message(chat_id=id, text=f'오늘의 날씨\n[{now.hour}시 00분 기준]')
        WL.weather(False)
        bot.send_photo(chat_id=id, photo=open('weather02.png', 'rb'))

    elif user_text == "식당" or user_text == "밥" or user_text == "학식" \
            or user_text == "ㅅㄷ" or user_text == "ㅂ" or user_text == "ㅎㅅ":
        WL.restaurant(False)
        bot.send_message(chat_id=id, text="이번주 식단입니다.")
        bot.send_photo(chat_id=id, photo=open('screenshot01.png', 'rb'))
        bot.send_photo(chat_id=id, photo=open('screenshot02.png', 'rb'))
    elif user_text == '학식 업데이트':
        WL.restaurant(True)
    else:
        try:
            bot.send_message(chat_id=id, text=eval(user_text))
        except:
            bot.send_message(chat_id=id, text="잘못된 명령어 입니다!")


# tim.sleep을 사용할 경우 실행이 어려움
schedule.every(60).seconds.do(job)

# Updater
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
updater.start_polling()

echo_handler = MessageHandler(Filters.text, handler)
dispatcher.add_handler(echo_handler)
schedule.run_pending()
