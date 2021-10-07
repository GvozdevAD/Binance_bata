# FloodWaitError -> https://docs.telethon.dev/en/latest/concepts/errors.html?highlight=FloodWaitError#avoiding-limits

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

API_ID = config["Telegram"]["api_id"]
API_HASH = config["Telegram"]["api_hash"]
USERNAME = config["Telegram"]["username"]

client = TelegramClient(USERNAME, API_ID, API_HASH)
client.start()

async def dump_all_messages(channel):
    """Записывает json-файл с информацией о всех сообщениях канала"""
    title = re.sub(r'[!"#$%&\'()*+,-./:;<=>?@\\^_`{|}~ ]', '', channel.title)

    # Получаем id последнего сообщения
    try:
        with open(f'Message_JSON\{title}.json', 'r', encoding='utf8') as file:
            data = json.load(file)
            min_id = data[0]['id']
            file.close()
    except:
        min_id = 0

    offset_msg = 0              # номер записи, с которой начинается считывание
    limit_msg = 100             # максимальное число записей, передаваемых за один раз

    new_messages = []           # список всех сообщений
    total_msg = 0
    total_count_limit = 100     # Колличестов запросов !!!!!ПОТОМ ПОМЕНЯТЬ!!!!!!!!


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
            min_id = min_id,
            hash = 0
        ))
    
        if not history.messages:
            break
        messages = history.messages

        if min_id == messages[0].id:
            break

        for msg in messages:
            try:
                if len(msg.message) > 0:
                    message = re.sub("^\s+|\n|\r|\s+$", ' ', str(msg.message))
                    new_messages.append({
                        'id' : msg.id,
                        'message' : message,
                        'date' : msg.date,
                        'status' : 'new'
                        })
            except :
                continue
        offset_msg = messages[len(messages) - 1].id
        total_msg = len(new_messages)

        if total_count_limit != 0 and total_msg >= total_count_limit:
            break

    if len(new_messages) != 0:
        if len(data) != 0:
            all_messages = new_messages + data
        else: all_messages = new_messages

        with open(f'Message_JSON\{title}.json', 'w', encoding='utf8') as file:
            json.dump(all_messages, file, ensure_ascii=False, indent = 4, cls=DateTimeEncoder)
            file.close()

async def main():
    with open('Source\links_telegram.txt', 'r') as file:
        links = str(file.read()).split('\n')
        file.close()

    for link in links:
        channel = await client.get_entity(link)
        await dump_all_messages(channel)


with client:
    #client.flood_sleep_threshold = 24 * 60 * 60
    client.loop.run_until_complete(main())
