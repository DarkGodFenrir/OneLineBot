# This Python file uses the following encoding: utf-8
import telebot
import param
import asyncio
from telethon_get import *
from sqlline import *
from keys import *

from telethon.sync import TelegramClient
from telethon import connection, functions, types, sync


bot = telebot.TeleBot(param.TOKEN)


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
        if Sqldb.grup_plus(message.chat.id) is True: print("Привлюсовал")
    else:
        bot.send_message(message.chat.id,"Канал уже добавлен в ваш список")

bot.polling()
