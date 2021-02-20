import telebot
from telebot import types

class Keys:

    def main_keys():
        markup  = types.ReplyKeyboardMarkup(True,True)
        button1 = types.KeyboardButton('⭕️Помощ')
        button2 = types.KeyboardButton('➕Добавить канал')
        button3 = types.KeyboardButton('👤Личный кабинет')
        button4 = types.KeyboardButton('🔖Список каналов')

        markup.row(button1,button2)
        markup.row(button3,button4)
        return (markup)
