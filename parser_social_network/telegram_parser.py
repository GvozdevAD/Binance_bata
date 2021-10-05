import configparser
import json
import re
import os
from pathlib import Path
# для корректного переноса времени сообщений в json
from datetime import datetime
from telethon.sync import TelegramClient
# Класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest



config = configparser.ConfigParser()
config_path = str(Path(__file__).parents[1]) + '\config.ini'
config.read(config_path)

api_id = config["Telegram"]["api_id"]
api_hash = config["Telegram"]["api_hash"]
username = config["Telegram"]["username"]

client = TelegramClient(username, api_id, api_hash)
client.start()

async def dump_all_messages(channel):
    """ """
    offset_msg = 0          # номер записи, с которой начинается считывание
    limit_msg = 100         # максимальное число записей, передаваемых за один раз

    all_messages = []       # список всех сообщений
    total_msg = 0
    total_count_limit = 15  # Колличестов выгружаемых сообщений !!!!!ПОТОМ ПОМЕНЯТЬ!!!!!!!!
    title = re.sub(r'[!"#$%&\'()*+,-./:;<=>?@\\^_`{|}~ ]', '', channel.title)

    class DateTimeEncoder(json.JSONEncoder):
        """Класс для сериализации записи дат в JSON"""
        def default(self, o):
            if isinstance(o, datetime):
                return o.isoformat()
            if isinstance(o, bytes):
                return list(o)
            return json.JSONEncoder.default(self, o)
    
    while True:
        history = await client(GetHistoryRequest(
            peer = channel,
            offset_id = offset_msg,
            offset_date = None,
            add_offset = 0,
            limit = limit_msg,
            max_id = 0,
            min_id = 0,
            hash = 0
        ))
    
        if not history.messages:
            break
        messages = history.messages
        for msg in messages:
            all_messages.append(msg.to_dict())
        offset_msg = messages[len(messages) - 1].id
        total_msg = len(all_messages)

        if total_count_limit != 0 and total_msg >= total_count_limit:
            break
    with open(f'{title}.json', 'w', encoding='utf8') as file:
        json.dump(all_messages, file, ensure_ascii=False, indent = 4, cls=DateTimeEncoder)

async def main():
    channel = await client.get_entity('https://t.me/procent_ru')
    await dump_all_messages(channel)

with client:
    client.loop.run_until_complete(main())
