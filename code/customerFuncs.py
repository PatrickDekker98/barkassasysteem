from main import *

def returnAllCustomers():
    customersData = cursor.execute('SELECT firstName, insertion, lastName, customerId FROM customer')
    customers = dict()
    for customer in customersData:
        customers[customer[3]] = [customer[0], customer[2], customer[1]]
    
    return customers

def returnOneCustomer(customerId):
    customerData = cursor.execute('SELECT firstName, insertion, lastName FROM customer WHERE customerId = ?', customerId)
    for customer in customerData:
        customerReturn = [customer[0], customer[2], customer[1]]

    return customerReturn

def returnAllTelegramIds():
    telegramIds = cursor.execute('SELECT telegramId FROM customer WHERE telegramId IS NOT NULL')
    returnIds = list()
    for Ids in telegramIds:
        returnIds.append(Ids[0])
    return returnIds

def unsetDb(customerId):
    cursor.execute('DELETE FROM customer WHERE customerId = ?', (str(customerId)))
    conn.commit()

def deactivateCustomer(customerId, confirm = False):
    if confirm:
        unsetDb(customerId)

def insertDb(customerId, firstName, insertion, lastName):
    if insertion == '':
        insertion = None
    cursor.execute('UPDATE customer SET firstName = ?, insertion = ?, lastName= ? WHERE customerID = ?', (firstName, insertion, lastName, customerId))
    conn.commit()

def editCustomer(customerId, firstName, insertion, lastName, confirm = False):
    if confirm:
       insertDb(customerId, firstName, insertion, lastName)

#addCustomer adds customer, if insertion is an empty string it replaces it with a NULL value, balance is standard 0 when creating a new customer
def addCustomer(firstName, insertion, lastName):
    balance = 0.0
    if insertion == '':
        insertion = None

    cursor.execute('INSERT INTO customer (firstName, insertion, lastName, balance) VALUES (?,?,?,?)', (firstName, insertion, lastName, balance))
    conn.commit()


