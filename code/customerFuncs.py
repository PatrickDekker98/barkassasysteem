from main import *


def returnAllCustomers():
    'Fetches and returns all customers'
    customersData = cursor.execute('SELECT firstName, insertion, lastName, customerId, balance, telegramId FROM customer')
    customers    = dict()
    for customer in customersData:
        customers[customer[3]] = [customer[0], customer[2], customer[1], customer[4], customer[5]]
    return customers


def returnOneCustomer(customerId):
    'takes a customerId, and returns the customers name'
    customerData = cursor.execute('SELECT firstName, insertion, lastName FROM customer WHERE customerId = ?', customerId)
    for customer in customerData:
        customerReturn = [customer[0], customer[2], customer[1]]

    return customerReturn


def returnAllTelegramIds():
    'Returns all documented telegram IDs'
    telegramIds = cursor.execute('SELECT telegramId FROM customer WHERE telegramId IS NOT NULL')
    returnIds = list()
    for Ids in telegramIds:
        returnIds.append(Ids[0])
    return returnIds


def addTelegramId(customerId, telegramId):
    'Add a customers Telegram ID to the database'
    cursor.execute('UPDATE customer SET telegramId = ? WHERE customerId = ?', (telegramId, customerId))
    conn.commit()


def unsetDb(customerId):
    'Deletes a customer from the database'
    cursor.execute('DELETE FROM customer WHERE customerId = ?', (str(customerId)))
    conn.commit()


def deactivateCustomer(customerId, confirm = False):
    'If confirmation is given, the customer will be deleted from the database. Takes a customerId, and optionally the confirmation in Boolian'
    if confirm:
        unsetDb(customerId)


def insertDb(customerId, firstName, insertion, lastName):
    'Edits a customer in the database'
    if insertion == '':
        insertion = None
    cursor.execute('UPDATE customer SET firstName = ?, insertion = ?, lastName= ? WHERE customerID = ?', (firstName, insertion, lastName, customerId))
    conn.commit()


def editCustomer(customerId, firstName, insertion, lastName, confirm = False):
    'Checks for confirmation before customer information in database is altered'
    if confirm:
       insertDb(customerId, firstName, insertion, lastName)


def addCustomer(firstName, insertion, lastName):
    'adds customer, if insertion is an empty string it replaces it with a NULL value, balance is standard 0 when creating a new customer'
    balance = 0.0
    if insertion == '':
        insertion = None

    cursor.execute('INSERT INTO customer (firstName, insertion, lastName, balance) VALUES (?,?,?,?)', (firstName, insertion, lastName, balance))
    conn.commit()


