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
from mysql import *
# from sqlline import *
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
    for gru in max_grup:
        param_g = Sqldb.get_param(gru)
        messages = []
        if len(param_g['title']) > 0:
            messages = asyncio.run(Tele.main(param_g))

        if len(messages) > 0:
            try:
                for mess in messages:
                    global group_id
                    if str(mess['grouped_id']) == "None" or str(mess['grouped_id']) != str(group_id):

                        linkgrup_m = "https://t.me/" + str(param_g['title']) +"/" + str(mess['id'])
                        linkgrup = "https://t.me/" + str(param_g['title']) +"/"
                        media = mess['media']
                        if media != None:
                            for user in param_g['users']:
                                try:
                                    if media['_'] == 'MessageMediaWebPage':
                                        url = media['webpage']
                                        url = url['url']
                                        sock = '<a href = "' + str(url) + '">' + '|' + "</a>"
                                        sock = str(sock) + '<a href = "'+ str(linkgrup_m) +'">' + str(param_g["nazv"]) + "</a>"
                                        mtext = str(sock) + '\n\n'+ str(mess['message'])
                                        bot.send_message(user, mtext, parse_mode='HTML')
                                    else:
                                        sock = '<a href = "'+ str(linkgrup_m) +'">' + str(param_g["nazv"]) + "</a>"
                                        mtext = str(sock) + '\n\n'+ str(mess['message'])
                                        bot.send_message(user, mtext, parse_mode='HTML')
                                except:
                                    e = sys.exc_info()[1]
                                    if str(e.args[0]).find('bot was blocked by the user') > -1:
                                        Sqldb.block_user(user)
                                        delgrup = Sqldb.get_grup(user)
                                        if delgrup != None and delgrup != "None":
                                            delgrup = delgrup.split()
                                            if "None" in delgrup:
                                                delgrup.remove("None")
                                            if "None_p" in delgrup:
                                                delgrup.remove("None_p")
                                        for dell in delgrup:
                                            if str(dell).find("_p") > -1:
                                                param_for_dell = ["del", str(dell)[len(str(dell))-2:], "p",user]
                                            else:
                                                param_for_del = ["del", dell, user]
                                            print(param_for_del)
                                            Sqldb.edit_list(param_for_del)
                                    else:
                                        e = sys.exc_info()[1]
                                        text = "Произошла ошибка: " + str(e.args[0])
                                        print(mess)
                                        bot.send_message(param.AUTHOR_ID, text)
                                        print(str(sys.exc_info()))

                        else:
                            for user in param_g['users']:
                                try:
                                    sock = '<a href = "'+ str(linkgrup) +'">' + str(param_g["nazv"]) + "</a>"
                                    bot.send_message(user,str(sock) + "\n\n" +str(mess['message']),
                                    parse_mode='HTML', disable_web_page_preview=True)
                                except:
                                    e = sys.exc_info()[1]
                                    if str(e.args[0]).find('bot was blocked by the user') > -1:
                                        Sqldb.block_user(user)
                                        delgrup = Sqldb.get_grup(user)
                                        if delgrup != None and delgrup != "None":
                                            delgrup = delgrup.split()
                                            if "None" in delgrup:
                                                delgrup.remove("None")
                                            if "None_p" in delgrup:
                                                delgrup.remove("None_p")
                                        for dell in delgrup:
                                            if str(dell).find("_p") > -1:
                                                param_for_del = ["del", str(dell)[len(str(dell))-2:], "p", user]
                                            else:
                                                param_for_del = ["del", dell, user]
                                            print(param_for_del)
                                            Sqldb.edit_list(param_for_del)
                                    else:
                                        e = sys.exc_info()[1]
                                        text = "Произошла ошибка: " + str(e.args[0])
                                        print(mess)
                                        bot.send_message(param.AUTHOR_ID, text)
                                        print(str(sys.exc_info()))

                        if 'grouped_id' in mess:
                            group_id = mess['grouped_id']
                    else:
                        continue
                if len(messages) > 0:
                    global num_messages
                    num_messages += len(messages)
            except:
                e = sys.exc_info()[1]
                text = "Произошла ошибка: " + str(e.args[0])
                print(mess)
                bot.send_message(param.AUTHOR_ID, text)
                print(str(sys.exc_info()))

def info_print():
    global num_messages
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(time + ": Отправленно", num_messages, "постов")
    num_messages = 0

def reclam():
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(time + ": время рекламы")
    user = Sqldb.get_user().split()
    print(user)
    # for us in user:
    #     bot.send_message(us,"Здесь могла бы быть ваша реклама\nВсе вопросы: @Maxidik")

@bot.message_handler(commands=['start'])
def start_message(message):

    user = [message.chat.id, message.chat.username]
    prov = Sqldb.r_users(user)
    key = Keys.main_keys()

    if prov is True:
        bot.send_message(message.chat.id, 'С возвращением!', reply_markup = key)
    else:
        if len(message.text.split())>1 and int(message.text.split()[1]) > 0:
            check = Sqldb.add_ref(message.text.split()[1])
            if check:
                text = "Была использована ваша реферальная ссылка, максимальное число каналов увеличено"
                bot.send_message(message.text.split()[1],text)
            else:
                text = "Была использована ваша реферальная ссылка. Рефералов до слота 1/2"
                bot.send_message(message.text.split()[1],text)
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
        if grup_g != None and grup_g != "None":
            grup_g = grup_g.split()
            if "None" in grup_g:
                grup_g.remove("None")
            if "None_p" in grup_g:
                grup_g.remove("None_p")
            grup_list = []
            for grup in grup_g:
                paramet = Sqldb.get_grup_param(grup)
                if paramet['g_id'] == "":
                    paramet['nazv'] = "Канал удален"
                    paramet['g_id'] = grup
                grup_list.append(paramet)
            print("====",message.chat.username,sep="\n",end=": \n")
            for grup in grup_list:
                print(grup['title'],grup['nazv'],sep="/")
            print('====')
            key = Keys.grup_list_keys(grup_list,message.chat.id)
            bot.send_message(message.chat.id,"Ваш список каналов: ",
            reply_markup=key)
        else:
            key = Keys.main_keys()
            bot.send_message(message.chat.id,"У вас нет активных групп",
            reply_markup = key)

    elif message.text == "⭕️Помощь":
        key = Keys.main_keys()
        text = "Данный бот создан для объединения новостей из разных групп в одну новостную линию. \nПо всем имеющимся вопросам обращаться - @Maxidik"
        bot.send_message(message.chat.id, text, reply_markup=key)
    elif message.text == "👤Личный кабинет":
        key = Keys.main_keys()
        paramet = Sqldb.get_us_param(message.chat.id)
        dop = int(paramet['refers'])%2
        if dop == 0:
            dop = 2
        refurl = "http://t.me/" + param.BOT_NAME + "?start=" + str(message.chat.id)
        text = "Рефералов: %s \nРефералов до получения слота группы: %s \nВаша реферальная ссылка: \n%s \nБаланс: %s"%(paramet['refers'], dop, refurl, paramet['balans'])
        bot.send_message(message.chat.id, text, reply_markup=key)
    elif message.text == "-q":
        if str(message.chat.id) == str(param.AUTHOR_ID):
            print('Можно остановить')
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
        bot.send_message(message.chat.id,"Канал добавлен, с этого момента вы будете получать НОВЫЕ посты канала")
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
        bot.send_message(callback_query.from_user.id, "Канал успешно удален")
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
    if rez[0] == 2:
        if rez[1]:
            asyncio.run(Tele.main(rez[2]))
        bot.send_message(callback_query.from_user.id, "Канал успешно запущен")
    else:
        print("Ошибка изменения листа")
    bot.answer_callback_query(callback_query.id)


if __name__ == "__main__":
    global group_id
    group_id = None

    global num_messages
    num_messages = 0
    schedule.every(15).seconds.do(function_to_run)
    schedule.every(1).minutes.do(function_to_run)
    schedule.every(1).hour.do(info_print)
    schedule.every().day.at("12:00").do(reclam)
    schedule.every().day.at("15:00").do(reclam)
    schedule.every().day.at("18:00").do(reclam)
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
