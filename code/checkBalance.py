from main import *


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
    totalSpent = round(cursor.fetchone()[0], 2)
    cursor.execute("SELECT sum(amount) as amount FROM balanceRaising WHERE customerId = ?", [customerId])
    totalPayed = round(cursor.fetchone()[0], 2)
    calculatedBalance = round(totalPayed - totalSpent, 2)
    return calculatedBalance


def correctBalance(customerId):
    """Corrects the balance column in the customer table to the calculated balance from the transaction history"""
    newBalance = getBalanceFromHistory(customerId)
    cursor.execute("UPDATE customer SET balance = ? WHERE customerId = ?", [newBalance, customerId])


correctBalance(1)
print(checkBalance(1))
