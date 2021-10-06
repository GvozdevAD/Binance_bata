# Жду ответ на получение АПИ 
# TWITTER гадский гад не дает апишечку!!!!!
# Использовать twython но это не точно
import json
import configparser
from pathlib import Path 
from twython import Twython


config = configparser.ConfigParser()
config_path = str(Path(__file__).parents[1]) + '\config.ini'
config.read(config_path)

APP_KEY = config['Twitter']['app_key']
APP_SECRET = config['Twitter']['app_secret']

