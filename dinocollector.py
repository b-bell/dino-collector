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
login_time_mins = int(config['DEFAULT']['LoginTimeMins'])
collection_time_hrs = int(config['DEFAULT']['CollectionTimeHours'])
days = int(config['DEFAULT']['Days'])
channel_dict = json.loads(config['DEFAULT']['ChannelsAndCommands'])
message_box_xpath = config['DEFAULT']['MessageBoxXPath']

# Perform conversions
login_time_secs = login_time_mins * 60
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
        time.sleep(5)
        text_element = driver.find_element_by_xpath(message_box_xpath)
        text_element.send_keys(channel_dict[channel_url])
        text_element.send_keys(Keys.ENTER)

    if i != iterations - 1:
        time.sleep(collection_time_secs)
        print(collection_time_secs)