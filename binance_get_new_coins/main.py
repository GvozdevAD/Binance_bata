import sys
import os
import schedule
import time
import json
from binance.client import Client
from pathlib import Path
from configparser import ConfigParser


def check_coins_in_txt():
    pass

def get_new_coin(list_coins):
    """Принимаем список полученных новых койнов
    и сравниваем новый список и старый"""

    path_txt = os.path.abspath('coins.txt')

    if os.path.exists(path_txt):
        with open(path_txt, 'r') as file:                   # Открываем файл с сохраненными койнами
            old_coins = str(file.read()).split('\n')        # и добавляем в переменную
            file.close()

        new_coins = list(set(old_coins) ^ set(list_coins))  # Сравниваем два списка и ищем новые койны

        if len(new_coins) > 0:                              # Если койны есть то записываем их в файлик
            print('[INFO] Found new coin')
            with open(path_txt, 'a') as file:
                file.write('\n' + '\n'.join(new_coins))
                file.close()
            
            return new_coins
        else:
            print('[INFO] Not Found')

    else:
    
        with open(path_txt, 'w') as file:
            file.write('\n'.join(list_coins))
            file.close()

def leave_an_order(client, new_coins):
    for coin in new_coins:
        symbol_info = client.get_symbol_info(coin)
        #print(json.dumps(symbol_info, indent=2))
    pass

def main():
    config = ConfigParser()
    path = Path(__file__).parents[1]
    config_path = str(path) + '\config.ini'
    config.read(config_path)
   
    api_key = config['Binance']['api_key']
    secret_key = config['Binance']['secret_key']
    client = Client(api_key, secret_key)                # Создаем клиента и передаем API ключи

    all_coin = client.get_all_tickers()                 # Получаем все койны что есть на бирже
    biance_coins = [ele['symbol'] for ele in all_coin]
    new_coins = get_new_coin(biance_coins)
    if new_coins != None:
        leave_an_order(client, new_coins)
    
    client.close_connection()
    
if __name__ == '__main__':
    schedule.every(2).seconds.do(main)                  # Запускаем скрипт каждые 5 секунд
    while True:
        schedule.run_pending()
        time.sleep(1)

