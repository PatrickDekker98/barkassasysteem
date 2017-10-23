from main import *
from customerFuncs import returnAllTelegramIds
import telepot
def sendToAll(msg) :
    token = '466467969:AAHZ253Zam0jPyJaqTxQZ6baCbWnvatsxt4'
    bot = telepot.Bot(token)
    telegramIs = returnAllTelegramIds()
    for telegramId in telegramIds:
        bot.sendMessage(telegramId, str(msg))


