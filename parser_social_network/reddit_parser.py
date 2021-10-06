# Ищу решение
import json
import configparser
import re
import requests
from pathlib import Path


def get_headers_reddit():
    config = configparser.ConfigParser()
    config_path = str(Path(__file__).parents[1]) + '\config.ini'
    config.read(config_path)
    
    CLIENT_ID = config['Reddit']['client_id']
    SECRET_TOKEN = config['Reddit']['secret_token']
    USERNAME = config['Reddit']['username']
    PASSWORD = config['Reddit']['pass']
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_TOKEN)
    data = {
        'grant_type' : 'password',
        'username' : USERNAME,
        'password' : PASSWORD
    }
    headers = {'User-Agent' : 'Gvozdev/0.0.1'}
    res = requests.post('https://www.reddit.com/api/v1/access_token', 
                        auth=auth, data=data, headers=headers)

    TOKEN = res.json()['access_token']
    headers = {**headers,**{'Authorization': f"bearer {TOKEN}"}}
    return headers

def main():
    headers = get_headers_reddit()
    res = requests.get('https://oauth.reddit.com/r/CryptoCurrency/',
                   headers=headers)
    with open('test.json', 'w', encoding='utf8') as file:
        json.dump(res.json(), file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()
