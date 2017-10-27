from main import *

#deze functie geeft alle klanten met alle data terug
def returnAllCustomers():
    customersData = cursor.execute('SELECT firstName, insertion, lastName, customerId, balance, telegramId FROM customer')
    customers    = dict()
    for customer in customersData:
        customers[customer[3]] = [customer[0], customer[2], customer[1], customer[4], customer[5]]
    
    return customers

#deze functie geef aleen de naam van een klant terug
def returnOneCustomer(customerId):
    customerData = cursor.execute('SELECT firstName, insertion, lastName FROM customer WHERE customerId = ?', customerId)
    for customer in customerData:
        customerReturn = [customer[0], customer[2], customer[1]]

    return customerReturn

#deze functie geeft alle telegram ids terug
def returnAllTelegramIds():
    telegramIds = cursor.execute('SELECT telegramId FROM customer WHERE telegramId IS NOT NULL')
    returnIds = list()
    for Ids in telegramIds:
        returnIds.append(Ids[0])
    return returnIds

#nu kan je een nieuw telegram id koppelen met een klant
def addTelegramId(customerId, telegramId):
    cursor.execute('UPDATE customer SET telegramId = ? WHERE customerId = ?', (telegramId, customerId))
    conn.commit()

#dit verwijderd een klant uit de database
def unsetDb(customerId):
    cursor.execute('DELETE FROM customer WHERE customerId = ?', (str(customerId)))
    conn.commit()

#alleen als confirm als true word meegegeven kan de klant worden verwijderd
def deactivateCustomer(customerId, confirm = False):
    if confirm:
        unsetDb(customerId)

#werk een klant bij, als inserion een lege string is word het none
def insertDb(customerId, firstName, insertion, lastName):
    if insertion == '':
        insertion = None
    cursor.execute('UPDATE customer SET firstName = ?, insertion = ?, lastName= ? WHERE customerID = ?', (firstName, insertion, lastName, customerId))
    conn.commit()

#alleen als confirm als true word meegegeven kan een klant worden bewerkt
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


