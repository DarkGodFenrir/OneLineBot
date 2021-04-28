import telebot
from telebot import types


class Keys:

    def main_keys():
        markup = types.ReplyKeyboardMarkup(True, True)
        button1 = types.KeyboardButton('👤Личный кабинет')
        button2 = types.KeyboardButton('➕Добавить канал')
        button3 = types.KeyboardButton('⭕️Помощь')
        button4 = types.KeyboardButton('🔖Список каналов')

        markup.row(button1, button2)
        markup.row(button3, button4)
        return markup

    def group_list_keys(self, telegram_id):
        markup = types.InlineKeyboardMarkup()

        for i in range(len(self)):
            param = self[i]
            button1 = types.InlineKeyboardButton(text=param['name'],
                                                 url="https://t.me/%s" % param['tag'])
            if str(param['group_id']).find("_p") > -1:
                button2 = types.InlineKeyboardButton(text='▶️',
                                                     callback_data='beg_%s_%s' % (param['group_id'], telegram_id))
            else:
                button2 = types.InlineKeyboardButton(text='⏸',
                                                     callback_data='pau_%s_%s' % (param['group_id'], telegram_id))
            button3 = types.InlineKeyboardButton(text='🗑',
                                                 callback_data='del_%s_%s' % (param['group_id'], telegram_id))
            markup.row(button1, button2, button3)

        return markup
