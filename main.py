from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from retry import retry
import constant
import time
import logging

@retry(tries=constant.COMMAND_TRIES,delay=constant.COMMAND_WAIT_SECS)
def write_command(message_box_xpath, command):
    text_element = driver.find_element(By.XPATH, message_box_xpath)
    text_element.send_keys(command)
    text_element.send_keys(Keys.ENTER)

if __name__ == '__main__':
    # Initiate chrome driver with unecessary default switches excluded
    service = ChromeService(executable_path=ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=service, options=options)

    # Let user log in to Discord
    driver.get(constant.DISCORD_LOGIN_URL)
    driver.execute_script(
        "alert('Welcome to the Dino Collector! You have " +
        str(constant.LOGIN_TIME_SECS) +
        " seconds to log in. Otherwise, the program will exit. This can be changed in the" +
        " config.ini file in your installation folder.');"
    )
    time.sleep(constant.LOGIN_TIME_SECS)

    # Get to work
    for i in range(constant.ITERATIONS):
        channel_list = list(constant.CHANNEL_DICT.keys())
        for channel_url in channel_list:
            driver.get(channel_url)
            try:
                write_command(constant.MESSAGE_BOX_XPATH, constant.CHANNEL_DICT[channel_url])
            except:
                logging.basicConfig(
                    filename='error.log',
                    encoding='utf-8',
                    level=logging.ERROR,
                    format='%(asctime)s %(message)s'
                )
                logging.exception('Dino Bot was unable to write a command')
                quit()

        if i != constant.ITERATIONS - 1:
            time.sleep(constant.COLLECTION_TIME_SECS)