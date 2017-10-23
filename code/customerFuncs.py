from main import *

def returnAllCustomers():
    customersData = cursor.execute('SELECT firstName, insertion, lastName, customerId FROM customer')
    customers    = dict()
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

