import configparser
import json

config = configparser.ConfigParser()
config.read('config.ini')

LOGIN_TIME_SECS = int(config['GENERAL']['LoginTimeSecs'])
COLLECTION_TIME_SECS = int(config['GENERAL']['CollectionTimeHours']) * 60 * 60
ITERATIONS = int(int(config['GENERAL']['Days']) * 24 / int(config['GENERAL']['CollectionTimeHours']))
CHANNEL_DICT = json.loads(config['GENERAL']['ChannelsAndCommands'])
MESSAGE_BOX_XPATH = config['DEVELOPER']['MessageBoxXPath']
COMMAND_TRIES = int(config['DEVELOPER']['CommandTries'])
COMMAND_WAIT_SECS = int(config['DEVELOPER']['CommandWaitSecs'])
