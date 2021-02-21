# This Python file uses the following encoding: utf-8
import telebot
import param
from sqlline import *
from keys import *

from telethon.sync import TelegramClient
from telethon import connection

from datetime import date, datetime

from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch


bot = telebot.TeleBot(param.TOKEN)

api_id   = param.API_ID
api_hash = param.API_HASH
username = param.USERNAME

client = TelegramClient(username, api_id, api_hash)
client.start()

@bot.message_handler(commands=['start'])
def start_message(message):

    user = [message.from_user.id, message.from_user.username]
    prov = Sqldb.r_users(user)
    key = Keys.main_keys()

    if prov is True:
        bot.send_message(message.chat.id, 'С возвращением!', reply_markup = key)
    else:
        bot.send_message(message.chat.id, 'Доброго времени суток, этот бот создан для того, чтобы обьединить информацию из нескольких групп.', reply_markup = key)



bot.polling()
