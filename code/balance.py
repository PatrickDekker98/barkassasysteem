from main import *

def returnOneBalance(customerId):
    'Returns balance of one customer'
    balances = cursor.execute('SELECT balance FROM customer WHERE customerId = ?', (str(customerId)))
    for balance in balances:
        balance = balance[0]
    return balance

def updateBalance(customerId, addition):
    'updates balance of one customer'
    oldBalance = returnOneBalance(customerId)
    newBalance = float(oldBalance) + float(addition)
    cursor.execute('UPDATE customer SET balance = ? WHERE customerId = ?', (newBalance, str(customerId)))
    conn.commit()



