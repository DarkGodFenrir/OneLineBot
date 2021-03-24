# This Python file uses the following encoding: utf-8
import telebot
import param
import asyncio
import schedule
import time
import sys
import threading
from threading import Thread
from telethon_get import *
from sqlline import *
from keys import *

from telethon.sync import TelegramClient
from telethon import connection, functions, types, sync

bot = telebot.TeleBot(param.TOKEN)

def send_message():
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        schedule.run_pending()
        time.sleep(1)

def function_to_run():
    max_grup = Sqldb.get_max_grup()
    for i in range(int(max_grup) + 1):
        param_g = Sqldb.get_param(i)
        messages = []
        if len(param_g['title']) > 0:
            messages = asyncio.run(Tele.main(param_g))

        try:
            for mess in messages:
                global group_id
                if mess['grouped_id'] != None and mess['grouped_id'] != str(group_id):

                    linkgrup_m = "https://t.me/" + str(param_g['title']) +"/" + str(mess['id'])
                    linkgrup = "https://t.me/" + str(param_g['title']) +"/"
                    media = mess['media']
                    if media != None:
                        for user in param_g['users']:
                            if media['_'] == 'MessageMediaWebPage':
                                url = media['webpage']
                                url = url['url']
                                sock = '<a href = "' + str(url) + '">' + '|' + "</a>"
                                sock = str(sock) + '<a href = "'+ str(linkgrup_m) +'">' + str(param_g["nazv"]) + "</a>"
                                mtext = str(sock) + '\n\n'+ str(mess['message'])
                                bot.send_message(user, mtext, parse_mode='HTML')
                            else:
                                for user in param_g['users']:
                                    sock = '<a href = "'+ str(linkgrup_m) +'">' + str(param_g["nazv"]) + "</a>"
                                    mtext = str(sock) + '\n\n'+ str(mess['message'])
                                    bot.send_message(user, mtext, parse_mode='HTML')

                    else:
                        for user in param_g['users']:
                            sock = '<a href = "'+ str(linkgrup) +'">' + str(param_g["nazv"]) + "</a>"
                            bot.send_message(user,str(sock) + "\n\n" +str(mess['message']),
                            parse_mode='HTML', disable_web_page_preview=True)
                else:
                    linkgrup_m = "https://t.me/" + str(param_g['title']) +"/" + str(mess['id'])
                    linkgrup = "https://t.me/" + str(param_g['title']) +"/"
                    media = mess['media']
                    if media != None:
                        for user in param_g['users']:
                            if media['_'] == 'MessageMediaWebPage':
                                url = media['webpage']
                                url = url['url']
                                sock = '<a href = "' + str(url) + '">' + '|' + "</a>"
                                sock = str(sock) + '<a href = "'+ str(linkgrup_m) +'">' + str(param_g["nazv"]) + "</a>"
                                mtext = str(sock) + '\n\n'+ str(mess['message'])
                                bot.send_message(user, mtext, parse_mode='HTML')
                            else:
                                for user in param_g['users']:
                                    sock = '<a href = "'+ str(linkgrup_m) +'">' + str(param_g["nazv"]) + "</a>"
                                    mtext = str(sock) + '\n\n'+ str(mess['message'])
                                    bot.send_message(user, mtext, parse_mode='HTML')
                    else:
                        for user in param_g['users']:
                            sock = '<a href = "'+ str(linkgrup) +'">' + str(param_g["nazv"]) + "</a>"
                            bot.send_message(user,str(sock) + "\n\n" +str(mess['message']),
                            parse_mode='HTML', disable_web_page_preview=True)
                group_id = mess['grouped_id']

            if len(messages) > 0:
                print("Отправлено " + str(len(messages)) + " сообщений " + str(len(param_g['users'])) + " пользователям группы " + str(param_g['nazv']))
        except:
            e = sys.exc_info()[1]
            text = "Произошла ошибка: " + str(e.args[0])
            bot.send_message(param.AUTHOR_ID, text)
            print(str(param_g))

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
            " чтобы добавить новый, ведите ссылку на канал:"%
            (prov[0],prov[1]))
            bot.register_next_step_handler(message, addchanel)
        else:
            key = Keys.main_keys()
            bot.send_message(message.chat.id,"У вас сайчас максимальное"
            " количество каналов", reply_markup = key)
    elif message.text == "🔖Список каналов":
        grup_g = Sqldb.get_grup(message.chat.id)
        print(grup_g)
        if grup_g != None and grup_g != "None":
            grup_g = grup_g.split()
            grup_list = []
            for grup in grup_g:
                print(grup)
                param = Sqldb.get_grup_param(grup)
                if param['g_id'] == "":
                    param['nazv'] = "Канал удален"
                    param['g_id'] = grup
                grup_list.append(param)
            key = Keys.grup_list_keys(grup_list,message.chat.id)
            bot.send_message(message.chat.id,"Ваш список каналов: ",
            reply_markup = key)
        else:
            key = Keys.main_keys()
            bot.send_message(message.chat.id,"У вас нет активных групп",
            reply_markup = key)
    elif message.text == "-q":
        print('a')
        t.do_run = False
        t.join()
        global exit
        exit = False
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

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('del_'))
def process_callback_delgru_del(callback_query: telebot.types.CallbackQuery):
    # code = callback_query.data[-1]
    info = re.split("[_]", str(callback_query.data))
    rez = Sqldb.edit_list(info)
    if rez == 0:
        bot.send_message(callback_query.from_user.id, "Канал успешно удлен")
    else:
        print("Ошибка изменения листа")
    bot.answer_callback_query(callback_query.id)

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('pau_'))
def process_callback_delgru_del(callback_query: telebot.types.CallbackQuery):
    # code = callback_query.data[-1]
    info = re.split("[_]", str(callback_query.data))
    print(info)
    rez = Sqldb.edit_list(info)
    if rez == 1:
        bot.send_message(callback_query.from_user.id, "Канал успешно поставлен на паузу")
    else:
        print("Ошибка изменения листа")
    bot.answer_callback_query(callback_query.id)

@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('beg_'))
def process_callback_delgru_del(callback_query: telebot.types.CallbackQuery):
    # code = callback_query.data[-1]
    info = re.split("[_]", str(callback_query.data))
    print(info)
    rez = Sqldb.edit_list(info)
    if rez == 2:
        bot.send_message(callback_query.from_user.id, "Канал успешно запущен")
    else:
        print("Ошибка изменения листа")
    bot.answer_callback_query(callback_query.id)


if __name__ == "__main__":
    global group_id
    group_id = None
    #schedule.every(15).seconds.do(function_to_run)
    schedule.every(1).minutes.do(function_to_run)
    t = threading.Thread(target=send_message)
    t.start()
    global exit
    exit = True
    while exit:
        try:
            bot.polling(none_stop=True)
        except:
            e = sys.exc_info()[1]
            text = "Произошла ошибка: " + str(e.args[0])
            bot.send_message(param.AUTHOR_ID, text)
            time.sleep(15)
