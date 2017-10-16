import sqlite3 as sql

db = '../barkassasysteem.db'
conn = sql.connect(db)
cursor = conn.cursor()


def verifyCustomer(customerId, verificationMethodId, reference):
    try:
        cursor.execute('SELECT reference FROM verificationMethod WHERE customerId = ? AND verificationMethodId = ?', (customerId, verificationMethodId))
        data = cursor.fetchone()[0] # get first item from dataset: the reference
        return reference == data  # return true if the reference matches the parameter reference
    except:
        return False  # return false if the query returns an error


customerId = 1 # klant 1
verificationMethodId = 1 # QR-code
reference = "1234" # referentie voor verificatie

print(verifyCustomer(customerId, verificationMethodId, reference))

customerId = 2 # klant 1
verificationMethodId = 1 # QR-code
reference = "1234" # referentie voor verificatie

print(verifyCustomer(customerId, verificationMethodId, reference))

customerId = 1 # klant 1
verificationMethodId = 1 # QR-code
reference = "5678" # referentie voor verificatie

print(verifyCustomer(customerId, verificationMethodId, reference))
