import json
import sys
import exec_error
from datetime import datetime

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

import param
from mysql import *

# from sqlline import *

api_id = param.API_ID
api_hash = param.API_HASH
username = param.USERNAME


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, bytes):
            return list(o)
        return json.JSONEncoder.default(self, o)


class Tele:

    async def get_last_news(param, client):
        try:
            channel = '@' + param['tag']

            offset_msg = 0  # номер записи, с которой начинается считывание
            limit_msg = 100  # максимальное число записей, передаваемых за один раз
            messages = []

            last_id = param['last_number']
            all_messages = []  # список всех сообщений
            total_messages = 0
            total_count_limit = 0  # поменяйте это значение, если вам нужны не все сообщения

            while True:
                history = await client(GetHistoryRequest(
                    peer=channel,
                    offset_id=offset_msg,
                    offset_date=None,
                    add_offset=0,
                    limit=limit_msg,
                    max_id=0,
                    min_id=last_id,
                    hash=0
                ))

                if not history.messages:
                    break

                messages = history.messages

                for message in messages:
                    all_messages.append(message.to_dict())

                offset_msg = messages[len(messages) - 1].id
                total_messages = len(all_messages)

                if total_count_limit != 0 and total_messages >= total_count_limit:
                    break

            if len(messages) > 0:
                Sqldb.edit_number(messages[0].id, param)

            per_messages = []
            for i in range(len(all_messages)):
                per_messages.append(all_messages[(len(all_messages) - 1) - i])
            return per_messages
        except:
            print(sys.exc_info())
            Sqldb.block(param['tag'])
            return []

        # with open('channel_messages.json', 'w', encoding='utf8') as outfile:
        #    json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder)

    async def get_for_reg_group(message, client):
        try:
            channel = message.text

            offset_msg = 0  # номер записи, с которой начинается считывание
            limit_msg = 1  # максимальное число записей, передаваемых за один раз

            all_messages = []  # список всех сообщений
            total_messages = 0
            total_count_limit = 1  # поменяйте это значение, если вам нужны не все сообщения

            messages = []
            chats = []

            while True:
                history = await client(GetHistoryRequest(
                    peer=channel,
                    offset_id=offset_msg,
                    offset_date=None,
                    add_offset=0,
                    limit=limit_msg,
                    max_id=0,
                    min_id=0,
                    hash=0
                ))

                if not history.messages:
                    break

                messages = history.messages
                chats = history.chats

                for messages_in in messages:
                    all_messages.append(messages_in.to_dict())

                offset_msg = messages[len(messages) - 1].id
                total_messages = len(all_messages)

                if total_count_limit != 0 and total_messages >= total_count_limit:
                    break

            group = {'group_id': chats[0].id, 'name': chats[0].title,
                     'tag': chats[0].username, 'last_number': messages[0].id,
                     'telegram_id': message.chat.id, 'user_name': message.chat.username}

            if Sqldb.add_new_group(group):
                return 1
            else:
                return 2
        except:
            error = sys.exc_info()[1]
            exec_error.exec_error(error, [])
            return 3

    async def main(param):
        client = TelegramClient(username,
                                api_id,
                                api_hash)
        await client.start()

        messages = await Tele.get_last_news(param, client)
        for mess in messages:
            channel_id = mess['peer_id']
            await client.forward_messages(-1001487429647, mess['id'], channel_id['channel_id'])

        mem = []
        number = get_number()
        for i in range(len(messages)):
            mem.append(number + i + 1)
        if mem:
            edit_memory_number(mem[-1])

        await client.disconnect()
        return mem

    async def reg_group(message):
        client = TelegramClient(username,
                                api_id,
                                api_hash)
        await client.start()
        result = await Tele.get_for_reg_group(message, client)
        await client.disconnect()

        return result

# 1)современные сети и их защита SDN механизмы защиты из SPG
# 2)Беспроводные сети 5G, 6G механизмы защиты

# Технологии и системы
# 1)Техногия облочного вычисления и их защита
# 2)Система распределенного реестра (Blockchain)

# 1)Принцыпы построения и защита и средства защиты DB2
# 2) --//-- Oracle (!!!!)
