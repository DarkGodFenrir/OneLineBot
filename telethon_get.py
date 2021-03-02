from telethon.sync import TelegramClient
from telethon import connection, functions, types, sync
import param
import json
import asyncio


from datetime import date, datetime

from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

from telethon.tl.functions.messages import GetHistoryRequest

api_id   = param.API_ID
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

    async def get_last_news(message):
        channel = message.text

        offset_msg = 0    # номер записи, с которой начинается считывание
        limit_msg = 100   # максимальное число записей, передаваемых за один раз

        all_messages = []   # список всех сообщений
        total_messages = 0
        total_count_limit = 1  # поменяйте это значение, если вам нужны не все сообщения

        print('Точка остановы 1')
        while True:
            history = await client(GetHistoryRequest(
            peer = channel,
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

            for message in messages:
                all_messages.append(message.to_dict())

            offset_msg = messages[len(messages) - 1].id
            total_messages = len(all_messages)

            if total_count_limit != 0 and total_messages >= total_count_limit:
                break

            with open('channel_messages.json', 'w', encoding='utf8') as outfile:
                json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder)

    async def main(message):
        client = await TelegramClient(username,
        api_id,
        api_hash)
        client.connect()

        await Tele.get_last_news(message)






#1)современные сети и их защита SDN механизмы защиты из SPG
#2)Беспроводные сети 5G, 6G механизмы защиты

#Технологии и системы
#1)Техногия облочного вычисления и их защита
#2)Система распределенного реестра (Blockchain)

#1)Принцыпы построения и защита и средства защиты DB2
#2) --//-- Oracle (!!!!)