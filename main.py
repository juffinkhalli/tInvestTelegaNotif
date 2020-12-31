import os
import requests
# import config
import threading
import telegram
from telegram.ext import Updater

tInv_token = ''
telegram_token = ''
my_chat_id = ''

print('START')


def set_config():
    global tInv_token
    global telegram_token
    global my_chat_id
    if os.environ.get('HEROKU', False):
        tInv_token = os.getenv('tInv_token')
        telegram_token = os.getenv('telegram_token')
        my_chat_id = os.getenv('my_chat_id')
    else:
        # tInv_token = config.tInv_token
        # telegram_token = config.telegram_token
        # my_chat_id = config.my_chat_id
        print('Config installed')


def getPortfolio():
    req = requests.get('https://api-invest.tinkoff.ru/openapi/portfolio',
                       headers={'Authorization': 'Bearer ' + tInv_token})
    temp_res = req.json()['payload']['positions']
    temp_str = ''
    for i in temp_res:
        if i['instrumentType'] != 'Currency':
            temp_str += (i['name'] + ' ' +
                         str(int(i['balance']) * int(i['averagePositionPrice']['value'])) + ' ' +
                         str(i['expectedYield']['value']) + ' ' +
                         i['averagePositionPrice']['currency'] + '\n')
        else:
            temp_str += (i['name'] + ' ' +
                         str(i['balance']) + ' ' +
                         str(i['expectedYield']['value']) + ' ' +
                         i['averagePositionPrice']['currency'] + '\n')
    return temp_str


def sendPortfolio():
    print('message sending...')
    bot.send_message(my_chat_id, text=getPortfolio())
    threading.Timer(900, sendPortfolio).start()
    print('message send.')


set_config()
bot = telegram.Bot(telegram_token)
bot.send_message(my_chat_id, text='START')
sendPortfolio()
updater = Updater(telegram_token, use_context=True)
updater.start_polling()
updater.idle()
