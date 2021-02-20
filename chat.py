# This Python file uses the following encoding: utf-8
import telebot
import param
from keys import *

from telethon.sync import TelegramClient
from telethon import connection

from datetime import date, datetime

from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch


bot = telebot.TeleBot(param.TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    key = Keys.main_keys()
    bot.send_message(message.chat.id, 'Доброго времени суток, этот бот создан для того, чтобы обьединить информацию из нескольких групп.', reply_markup = key)





bot.polling()
