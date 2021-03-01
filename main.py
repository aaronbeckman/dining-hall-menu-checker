import atexit
import datetime
import json
import logging
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from web_driver import Web_Driver

######################### INITIALIZATION #########################

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s - %(levelname)s] %(message)s',
    handlers=[logging.FileHandler(
        filename='out.log'), logging.StreamHandler(sys.stdout)]
)


def exit_handler():
    logging.info('Exit handler called')
    try:
        w.close()
    except:
        logging.warning('Could not find Web_Driver instance to close')


atexit.register(exit_handler)

with open('constants.json') as f:
    constants = json.load(f)

market = constants["market_xpaths"]
meal = constants["meal_xpaths"]
next_day = constants["next_day_xpath"]
previous_day = constants["previous_day_xpath"]

######################### MAIN STUFF #########################

logging.info('Starting webdriver...')
w = Web_Driver()

w.select_location(market['Four Lakes'])
w.select_meal(meal['Breakfast'])
print(w.select_day(datetime.date(2021, 3, 7)))

time.sleep(6)
