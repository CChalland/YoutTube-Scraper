# encoding: utf-8
import os
from decouple import config
from datetime import datetime

SELENIUM_FIREFOX = '/Users/ColeChalland/Documents/Selenium/FireFox'

################################################################ PATHS ->
home = str(os.getcwd())

FILES_FOLDER = home + '/'
DATA_PATH = FILES_FOLDER + "data/"
LOGS_PATH = FILES_FOLDER + 'logs/'




MAX_WORKERS = 10 # max threads at a time

# YOUR API KEYS GO HERE!
# KEY = config('CLIENT_ID')
# SECRET_KEY = config('CLIENT_SECRET')