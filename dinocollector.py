from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import configparser
import json
import time
import os

# Initiate config file
config = configparser.ConfigParser()
config.read('config.ini')

# Collect config
login_time_secs = int(config['GENERAL']['LoginTimeSecs'])
collection_time_hrs = int(config['GENERAL']['CollectionTimeHours'])
days = int(config['GENERAL']['Days'])
channel_dict = json.loads(config['GENERAL']['ChannelsAndCommands'])
page_transition_time_secs = int(config['DEVELOPER']['PageTransitionTimeSecs'])
message_box_xpath = config['DEVELOPER']['MessageBoxXPath']

# Perform conversions
collection_time_secs = collection_time_hrs * 60 * 60
iterations = int(days * 24 / collection_time_hrs)

# Initiate chrome driver
PATH = os.getcwd() + '\chromedriver.exe'
driver = webdriver.Chrome(PATH)

# Login process
driver.get('https://discord.com/login')
time.sleep(login_time_secs)

# Get to work
for i in range(iterations):
    channel_list = list(channel_dict.keys())
    for channel_url in channel_list:
        driver.get(channel_url)
        time.sleep(page_transition_time_secs)
        text_element = driver.find_element_by_xpath(message_box_xpath)
        text_element.send_keys(channel_dict[channel_url])
        text_element.send_keys(Keys.ENTER)

    if i != iterations - 1:
        time.sleep(collection_time_secs)
        print(collection_time_secs)