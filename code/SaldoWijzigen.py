import sqlite3
import datetime
import tkinter

conn = sqlite3.connect('example.db')
c = conn.cursor()

def raiseBalance():

    amountIn = askAmount()

    datetime1 = datetime.date.today()

    c.execute('''SELECT balance FROM customer''')
    balans = c.fetchone()

    newBalance = balans + amountIn

    c.execute('''UPDATE balanceRaising SET amount = ? WHERE id = ? ''', (amount1))
    c.execute('''UPDATE customer SET balance  = ? WHERE id = ?''', (newBalance))
    c.execute(''''UPDATE ''')

    return

def askAmount():

    amountInput = Entry.get()

    return amountInput

#c.execute('''CREATE TABLE customer(balance REAL)''')
#c.execute('''CREATE TABLE balanceRaising(balanceRaisingId INTEGER, customerId INTEGER, amount REAL, datetime DATETIME)''')
#c.execute('''INSERT INTO balanceRaising(balanceRaisingId, customerId, amount, datetime) VALUES(?,?,?,?)''', (balanceRaisingId1, customerId1, amount1, datetime1, ))

raiseBalance()

conn.commit()