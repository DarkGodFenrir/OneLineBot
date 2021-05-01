# This Python file uses the following encoding: utf-8
import asyncio
import re
import threading
import time

import schedule

import exec_error
from keys import *
from mysql import *
from telethon_get import *

bot = telebot.TeleBot(param.TOKEN)

def send_message():
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        schedule.run_pending()
        time.sleep(1)


def function_to_run():
    max_group = get_max_group()
    for gru in max_group:
        param_g = Sqldb.get_param(gru)
        messages = []
        if len(param_g['tag']) > 0:
            messages = asyncio.run(Tele.main(param_g))

        if messages:
            global num_messages
            for number in messages:
                for user in Sqldb.get_users(param_g['group_id']):
                    try:
                        bot.forward_message(user, -1001487429647, number)
                    except:
                        error = sys.exc_info()[1]
                        exec_error.exec_error(error, user)
            num_messages = num_messages + len(messages)


def info_print():
    global num_messages
    info_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(info_time + ": Отправленно", num_messages, "постов")
    num_messages = 0


def advertising():
    ad_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(ad_time + ": время рекламы")
    user = Sqldb.get_user()
    print(user)
    # for us in user:
    #     bot.send_message(us,"Здесь могла бы быть ваша реклама\nВсе вопросы: @Maxidik")


@bot.message_handler(commands=['start'])
def start_message(message):
    user = [message.chat.id, message.chat.username]
    prov = Sqldb.login_user(user)
    key = Keys.main_keys()

    if prov is True:
        bot.send_message(message.chat.id, 'С возвращением!', reply_markup=key)
    else:
        if len(message.text.split()) > 1 and int(message.text.split()[1]) > 0:
            check = Sqldb.add_ref(message.text.split()[1])
            if check:
                use_referral_text = "Была использована ваша реферальная ссылка, максимальное число каналов увеличено"
                bot.send_message(message.text.split()[1], use_referral_text)
            else:
                use_referral_text = "Была использована ваша реферальная ссылка. Рефералов до слота 1/2"
                bot.send_message(message.text.split()[1], use_referral_text)
        bot.send_message(message.chat.id, 'Доброго времени суток, этот бот'
                                          ' создан для того, чтобы обьединить информацию из нескольких групп.',
                         reply_markup=key)


@bot.message_handler()
def get_message(message):
    if message.text == "➕Добавить канал":
        prov = Sqldb.channel_check(message.chat.id)

        if prov[0] < prov[1]:
            bot.send_message(message.chat.id, "У вас сейчас %s из %s каналов,"
                                              " чтобы добавить новый, ведите ссылку на канал:" %
                             (prov[0], prov[1]))
            bot.register_next_step_handler(message, add_channel)
        else:
            key = Keys.main_keys()
            bot.send_message(message.chat.id, "У вас сайчас максимальное"
                                              " количество каналов", reply_markup=key)

    elif message.text == "🔖Список каналов":
        group_g = Sqldb.get_group(message.chat.id)
        if group_g is not None and group_g != "None":
            print(group_g)
            print("====", message.chat.username, sep="\n", end=": \n")
            for group in group_g:
                print(group['tag'], group['name'], sep="/")
            print('====')
            key = Keys.group_list_keys(group_g, message.chat.id)
            bot.send_message(message.chat.id, "Ваш список каналов: ",
                             reply_markup=key)
        else:
            key = Keys.main_keys()
            bot.send_message(message.chat.id, "У вас нет активных групп",
                             reply_markup=key)

    elif message.text == "⭕️Помощь":
        key = Keys.main_keys()
        referral_text = "Данный бот создан для объединения новостей из разных групп в одну новостную линию. \nПо всем " \
                        "имеющимся вопросам обращаться - @Maxidik "
        bot.send_message(message.chat.id, referral_text, reply_markup=key)
    elif message.text == "👤Личный кабинет":
        key = Keys.main_keys()
        parameter = Sqldb.get_us_param(message.chat.id)
        dop = int(parameter['refers']) % 2
        if dop == 0:
            dop = 2
        ref_url = "http://t.me/" + param.BOT_NAME + "?start=" + str(message.chat.id)
        referral_text = "Рефералов: %s \nРефералов до получения слота группы: %s \nВаша реферальная ссылка: \n%s " \
                        "\nБаланс: %s" % (
                            parameter['refers'], dop, ref_url, parameter['balance'])
        bot.send_message(message.chat.id, referral_text, reply_markup=key)
    elif message.text == "-q":
        if str(message.chat.id) == str(param.AUTHOR_ID):
            print('Можно остановить')
            t.do_run = False
            t.join()
            global exit
            exit = False
    else:
        bot.send_message(message.chat.id, "Команда неизвестна или находится в разработке")


def add_channel(message):
    result = asyncio.run(Tele.reg_group(message))

    if result == 1:
        Sqldb.group_plus(message.chat.id)
        bot.send_message(message.chat.id, "Канал добавлен, с этого момента вы будете получать НОВЫЕ посты канала")
    elif result == 2:
        bot.send_message(message.chat.id, "Канал уже добавлен в ваш список")
    elif result == 3:
        bot.send_message(message.chat.id, "Бот не может получать посты этой группы")
    else:
        bot.send_message(message.chat.id, "Произошла неизвестная ошибка, группа не добавлена")


@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('del_'))
def process_callback_dell_group(callback_query: telebot.types.CallbackQuery):
    # code = callback_query.data[-1]
    info = re.split("[_]", str(callback_query.data))

    if Sqldb.edit_list(info) == 0:
        bot.send_message(callback_query.from_user.id, "Канал успешно удален")
    else:
        print("Ошибка изменения листа")
    bot.answer_callback_query(callback_query.id)


@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('pau_'))
def process_callback_dell_group(callback_query: telebot.types.CallbackQuery):
    # code = callback_query.data[-1]
    info = re.split("[_]", str(callback_query.data))

    if Sqldb.edit_list(info) == 1:
        bot.send_message(callback_query.from_user.id, "Канал успешно поставлен на паузу")
    else:
        print("Ошибка изменения листа")
    bot.answer_callback_query(callback_query.id)


@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('beg_'))
def process_callback_dell_group(callback_query: telebot.types.CallbackQuery):
    # code = callback_query.data[-1]
    info = re.split("[_]", str(callback_query.data))

    rez = Sqldb.edit_list(info)
    if rez['num'] == 2:
        if rez['flag']:
            asyncio.run(Tele.main(rez))
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
    schedule.every().day.at("12:00").do(advertising)
    schedule.every().day.at("15:00").do(advertising)
    schedule.every().day.at("18:00").do(advertising)
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
