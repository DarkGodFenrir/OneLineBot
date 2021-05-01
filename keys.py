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
        markup = types.InlineKeyboardMarkup(row_width=2)

        for i in range(len(self)):
            param = self[i]
            button1 = types.InlineKeyboardButton(text=param['name'],
                                                 url=f"https://t.me/{param['tag']}")
            if param['paused'] == 0:
                button2 = types.InlineKeyboardButton(text='⏸',
                                                     callback_data=f'pau_{param["group_id"]}_{telegram_id}')
            else:
                button2 = types.InlineKeyboardButton(text='▶️',
                                                     callback_data=f'beg_{param["group_id"]}_{telegram_id}')
            button3 = types.InlineKeyboardButton(text='🗑',
                                                 callback_data=f'del_{param["group_id"]}_{telegram_id}')
            markup.row(button1, button2, button3)

        return markup
