# This Python file uses the following encoding: utf-8
import telebot
import param
import asyncio
import schedule
import time
import io
from PIL import Image
from io import BytesIO
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
        param_g = Sqldb.get_param(i)
        messages = []
        if len(param_g['title']) > 0:
            messages = asyncio.run(Tele.main(param_g))
        for mess in messages:
            print(mess)
            media = mess['media']
            if media != None:
                if media['_'] == 'MessageMediaWebPage':
                    photo = media['webpage']
                    for user in param_g['users']:
                        bot.send_photo(user,str(photo['url']),
                        caption = str(mess['message']) + "\n\nИсточник: @" + str(param_g['title']))
                    # bot.send_mes(param.AUTHOR_ID, disable_web_page_preview= 'false',
                    # text='<a href= ' + str(photo['url'] + '> </a>' + str(mess['message'])),parse_mode= "HTML")
                elif media['_'] == 'MessageMediaPhoto':
                    photo = media['photo']
                    photo = photo['file_reference']
                    for user in param_g['users']:
                        bot.send_photo(user, photo = photo,
                        caption = str(mess['message']) + "\n\nИсточник: @" + str(param_g['title']))
                elif media['_'] == 'MessageMediaDocument':
                    document= media['document']
                    for user in param_g['users']:
                        bot.send_file(user,document['id'],
                        caption = str(mess['message']) + "\n\nИсточник: @" + str(param_g['title']))
                else:
                    print(media['_'])
            else:
                for user in param_g['users']:
                    bot.send_message(user, text=str(mess['message']) + "\n\nИсточник: @" + str(param_g['title']))
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
        bot.send_message(message.chat.id,"Команда неизвестна или находится в разработке")

def addchanel(message):

    result = asyncio.run(Tele.reg_grup(message))

    if result == 1:
        Sqldb.grup_plus(message.chat.id)
        bot.send_message(message.chat.id,"Канал добавлен, ждите новых постов")
    elif result == 2:
        bot.send_message(message.chat.id,"Канал уже добавлен в ваш список")
    elif result == 3:
        bot.send_message(message.chat.id,"Бот не может получать посты этой группы")
    else:
        bot.send_message(message.chat.id,"Произошла неизвестная ошибка, группа не добавлена")

if __name__ == "__main__":
    schedule.every(15).seconds.do(function_to_run)
    # schedule.every(1).minutes.do(function_to_run)
    Thread(target=send_message).start()
    bot.polling()
