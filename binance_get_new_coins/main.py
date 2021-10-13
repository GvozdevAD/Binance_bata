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

    path_json = os.path.abspath('coins.json')

    if os.path.exists(path_json):
        
        with open(path_json, 'r', encoding='utf8') as file: # Открываем файл с сохраненными койнами
            old_coins = json.load(file)                     # и добавляем в переменную
            file.close()

        new_coins = list(set(old_coins['coins']) ^ set(list_coins))  # Сравниваем два списка и ищем новые койны

        if len(new_coins) > 0:                              # Если койны есть то записываем их в файлик
            print('[INFO] Found new coin')
            with open(path_json, 'r',encoding='utf8') as file:
                all_coins = json.load(file)
                all_coins['coins']+=new_coins
                with open(path_json, 'w', encoding='utf8') as f:
                    json.dump(all_coins, f, ensure_ascii=False,indent=4)
                    f.close()
                file.close()
            
            return new_coins
        else:
            print('[INFO] Not Found')

    else:
        with open(path_json, 'w', encoding='utf8') as file:
            json.dump({'coins':list_coins}, file, ensure_ascii=False, indent=4)
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
   
    API_KEY = config['Binance']['api_key']
    SECRET_KEY = config['Binance']['secret_key']
    client = Client(API_KEY, SECRET_KEY)                # Создаем клиента и передаем API ключи

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

