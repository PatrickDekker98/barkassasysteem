from main import *


def checkBalance(customerId):
    balanceFromCustomer = getBalanceFromCustomer(customerId)
    balanceFromHistory = getBalanceFromHistory(customerId)


def getBalanceFromCustomer(customerId):
    cursor.execute("SELECT balance FROM customer WHERE customerId = 1")
    return cursor.fetchOne()[0]


def getBalanceFromHistory(customerId):
    cursor.execute("")
