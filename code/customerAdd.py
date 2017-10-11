#import only sqlite3
import sqlite3 as sql

#global variables
dataBaseAddr = '../barkassasysteem.db'

#addCustomer adds customer, if insertion is an empty string it replaces it with a NULL value, balance is standard 0 when creating a new customer
def addCustomer(firstName, insertion, lastName):
    #database setup
    conn    = sql.connect(dataBaseAddr)
    cursor  = conn.cursor()
    
    balance = 0.0
    if insertion == '':
        insertion = None

    cursor.execute('INSERT INTO customer (firstName, insertion, lastName, balance) VALUES (?,?,?,?)', (firstName, insertion, lastName, balance))
    conn.commit()
    conn.close()

#function call
addCustomer(input("firstname: "), input("insertion: "), input("firstname: "))
