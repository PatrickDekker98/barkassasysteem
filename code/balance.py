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


def checkBalance(customerId):
    """Compares the balance from the customer table with the balance calculated from the transaction history"""
    balanceFromCustomer = getBalanceFromCustomer(customerId)
    balanceFromHistory = getBalanceFromHistory(customerId)
    print(balanceFromCustomer)
    print(balanceFromHistory)
    return balanceFromHistory == balanceFromCustomer

def getBalanceFromCustomer(customerId):
    """Fetches the balance from the customer table"""
    cursor.execute("SELECT balance FROM customer WHERE customerId = ?", [customerId])
    return round(cursor.fetchone()[0], 2)


def getBalanceFromHistory(customerId):
    """Fetches the balance, calculated from the transaction history"""
    cursor.execute("SELECT SUM(p.amount * pr.value) AS total FROM customer c LEFT JOIN verificationMethod v ON c.customerId = v.customerId LEFT JOIN 'transaction' t ON v.verificationMethodId = t.verificationMethodId LEFT JOIN purchase p ON t.transactionId = p.transactionId LEFT JOIN price pr ON pr.productId = p.productId WHERE pr.datetimeStart < t.datetime  AND (pr.datetimeEnd > t.datetime OR pr.datetimeEnd IS NULL) AND c.customerId = ?", [customerId])
    total = cursor.fetchone()[0]
    if total != None:
        totalSpent = round(total, 2)
    else:
        totalSpent = 0
    cursor.execute("SELECT sum(amount) as amount FROM balanceRaising WHERE customerId = ?", [customerId])
    totalPayed = round(cursor.fetchone()[0], 2)
    calculatedBalance = round(totalPayed - totalSpent, 2)
    return calculatedBalance


def correctBalance(customerId):
    """Corrects the balance column in the customer table to the calculated balance from the transaction history"""
    newBalance = getBalanceFromHistory(customerId)
    cursor.execute("UPDATE customer SET balance = ? WHERE customerId = ?", [newBalance, customerId])
    conn.commit()


def writeNewTransaction(customerId, transaction):
    'writes a new transaction to the database'
    if checkBalance(customerId):
        print('if')
        customerBalance = getBalanceFromCustomer(customerId)
        total = 0
        for product in transaction:
            total += (product[1] * product[2])
        if customerBalance < total:
            tkinter.messagebox.showerror('Niet genoeg geld op rekening', 'Helaas heeft u niet voldoende geld op uw rekening staan voor deze bestelling. Graag eerst meer geld op uw rekening storten!')
            return False
        else:
            cursor.execute('''INSERT INTO 'transaction' (verificationMethodId, datetime) VALUES(4,datetime('now', 'localtime'))''')
            cursor.execute('''SELECT MAX(transactionId) FROM 'transaction' ''')
            transactionId = cursor.fetchone()[0]
            for product in transaction:
                cursor.execute('''INSERT INTO purchase(transactionId, productId, amount) VALUES (?, ?, ?)''', [transactionId, product[0],product[1]])
        correctBalance(customerId)
        return True
    else:
        print('else')
        correctBalance(customerId)
        return False
