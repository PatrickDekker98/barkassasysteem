#import only sqlite3
import sqlite3 as sql

#global variables
dataBaseAddr = '../barkassasysteem.db'

def confirmEdit(confirmStr):
    confirm = True 
    while confirm:
        cnfrm = input(confirmStr)
        if cnfrm.lower() == 'y' : 
            confirm = False
            returnBool = True
        elif cnfrm.lower() == 'n':
            confirm = False
            returnBool = False
        else:
            confirm = True
            print('please answer Y (Yes) or n (no)')
    return returnBool

def unsetDb(cId):
    c.execute('DELETE FROM customer WHERE customerId = ?', (cId))

def deactivateCustomer(cId):
    global c
    conn         = sql.connect(dataBaseAddr)
    c            = conn.cursor()
    customerData = c.execute('SELECT firstname, insertion, lastName, customerId FROM customer WHERE customerId = ?', cId)
    for customer in customerData:
        if customer[1] == None:
            confirmStr = 'Do you want to edit ' + customer[0] + ' ' + customer[2] + ' with id ' + str(customer[3]) + '? Y/n: '
        else :
            confirmStr = 'Do you want to edit ' + customer[0] + ' ' + customer[1] + ' ' + customer[2] + ' with id ' + str(customer[3]) + '? Y/n: '

    cont = confirmEdit(confirmStr)

    if cont:
        unsetDb(cId)
    else:
        print('no harm was done to our precious database')

    conn.commit()
    conn.close()

deactivateCustomer(input('id? '))
