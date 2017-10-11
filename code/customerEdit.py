#import only sqlite3
import sqlite3 as sql

#global variables
dataBaseAddr = '../barkassasysteem.db'

def confirmEdit(confirmStr):
    confirm = True 
    while confirm:
        cnfrm = input(confirmStr)
        if cnfrm.lower() == 'y':
            confirm = False
            returnBool = True
        elif cnfrm.lower() == 'n':
            confirm = False
            returnBool = False
        else:
            confirm = True
            print('please answer Y (Yes) or n (no)')
    return returnBool
        
def insertDb(cId):
    firstName  = input('fistname: ')
    insertion = input('insertion: ')
    lastName  = input('lastName: ')
    if insertion == '':
        insertion = None
    c.execute('UPDATE customer SET firstName = ?, insertion = ?, lastName= ? WHERE customerID = ?', (firstName, insertion, lastName, cId))


def editCustomer(cId):
    #database setup
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
        insertDb(cId)
    else: 
        print('no harm was done to our precious database')

    conn.commit()
    conn.close()
    
editCustomer(input('id?; '))
