# This Python file uses the following encoding: utf-8
import telebot
import param
import asyncio
import schedule
import time
from threading import Thread
from telethon_get import *
from sqlline import *
from keys import *

from telethon.sync import TelegramClient
from telethon import connection, functions, types, sync

bot = telebot.TeleBot(param.TOKEN)

def send_message():
    while True:
        schedule.run_pending()
        time.sleep(1)

def function_to_run():
    max_grup = Sqldb.get_max_grup()
    for i in range(int(max_grup) + 1):
        print(str(i) + ' = i')
        param_g = Sqldb.get_param(i)
        if param_g['title'] is not None:
            messages = asyncio.run(Tele.main(param_g))

    #return bot.send_message(param.AUTHOR_ID,"прошло 10 секунд")


@bot.message_handler(commands=['start'])
def start_message(message):

    user = [message.from_user.id, message.from_user.username]
    prov = Sqldb.r_users(user)
    key = Keys.main_keys()

    if prov is True:
        bot.send_message(message.chat.id, 'С возвращением!', reply_markup = key)
    else:
        bot.send_message(message.chat.id, 'Доброго времени суток, этот бот'
        ' создан для того, чтобы обьединить информацию из нескольких групп.',
         reply_markup = key)

@bot.message_handler()
def get_message(message):
    if message.text == "➕Добавить канал":
        prov = Sqldb.p_chanel(message.chat.id)

        if prov[0] < prov[1]:
            bot.send_message(message.chat.id,"У вас сейчас %s из %s каналов,"
            " чтобы добавить новый ведите ссылку на канал:"%
            (prov[0],prov[1]))
            bot.register_next_step_handler(message, addchanel)
        else:
            key = Keys.main_keys()
            bot.send_message(message.chat.id,"У вас сайчас максимальное"
            " количество каналов", reply_markup = key)
    else:
        bot.send_message(message.chat.id,"Неизвестная команда")

def addchanel(message):

    result = asyncio.run(Tele.reg_grup(message))

    if result is True:
        bot.send_message(message.chat.id,"Канал добавлен")
        if Sqldb.grup_plus(message.chat.id) is True:
            print("Привлюсовал")
    else:
        bot.send_message(message.chat.id,"Канал уже добавлен в ваш список")

if __name__ == "__main__":
    schedule.every(5).seconds.do(function_to_run)
    #schedule.every(1).minutes.do(function_to_run)
    Thread(target=send_message).start()
    bot.polling()
