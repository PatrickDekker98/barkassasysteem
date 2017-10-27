from main import *
from customerFuncs import returnAllTelegramIds
from telegramToCsv import write2csv
import telepot
def sendToAll(msg) :
    'Sends a message to all customers'
    token = '466467969:AAHZ253Zam0jPyJaqTxQZ6baCbWnvatsxt4'
    bot = telepot.Bot(token)
    telegramIds = returnAllTelegramIds()
    for telegramId in telegramIds:
        write2csv(telegramId, msg)
        bot.sendMessage(telegramId, str(msg))
