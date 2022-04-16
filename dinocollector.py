from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import configparser
import json
import time
import logging

# Initiate config file
config = configparser.ConfigParser()
config.read('config.ini')

# Collect config
login_time_secs = int(config['GENERAL']['LoginTimeSecs'])
collection_time_hrs = int(config['GENERAL']['CollectionTimeHours'])
days = int(config['GENERAL']['Days'])
channel_dict = json.loads(config['GENERAL']['ChannelsAndCommands'])
page_wait_time_secs = int(config['DEVELOPER']['PageWaitTimeSecs'])
message_box_xpath = config['DEVELOPER']['MessageBoxXPath']

# Perform conversions
collection_time_secs = collection_time_hrs * 60 * 60
iterations = int(days * 24 / collection_time_hrs)

# Initiate chrome driver with unecessary default switches excluded
service = Service(executable_path=ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=service, options=options)

# Login process
driver.get('https://discord.com/login')
driver.execute_script(
    "alert('Welcome to the Dino Collector! You have " +
    str(login_time_secs) +
    " seconds to log in. Otherwise, the program will exit. This can be changed in the" +
    " config.ini file in your installation folder.');"
)
time.sleep(login_time_secs)

# Get to work
for i in range(iterations):
    channel_list = list(channel_dict.keys())
    for channel_url in channel_list:
        driver.get(channel_url)
        time.sleep(page_wait_time_secs)
        try:
            text_element = driver.find_element(By.XPATH, message_box_xpath)
            text_element.send_keys(channel_dict[channel_url])
            text_element.send_keys(Keys.ENTER)
        except:
            logging.basicConfig(filename='error.log',
                encoding='utf-8',
                level=logging.ERROR,
                format='%(asctime)s %(message)s'
            )
            logging.exception('Dino Bot was unable to write a command')
            quit()

    if i != iterations - 1:
        time.sleep(collection_time_secs)