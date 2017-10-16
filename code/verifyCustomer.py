import sqlite3 as sql

db = '../barkassasysteem.db'
conn = sql.connect(db)
cursor = conn.cursor()


def verifyCustomer(customerId, verificationTypeId, reference):
    try:
        data = cursor.execute("SELECT reference FROM verificationMethod WHERE customerId = ? AND verificationTypeId = ? AND datetimeStart <= datetime('now', 'localtime') AND (datetimeEnd ISNULL OR datetimeEnd > datetime('now', 'localtime'))", (customerId, verificationTypeId))
        for row in data:
            if reference in row:
                return True
        return False
    except:
        return False  # return false if the query returns an error


customerId = 1  # klant 1
verificationTypeId = 1  # QR-code
reference = "8248"  # referentie voor verificatie

print(verifyCustomer(customerId, verificationTypeId, reference))

customerId = 2  # klant 1
verificationTypeId = 1  # QR-code
reference = "1234"  # referentie voor verificatie

print(verifyCustomer(customerId, verificationTypeId, reference))

customerId = 1  # klant 1
verificationTypeId = 1  # QR-code
reference = "5678"  # referentie voor verificatie

print(verifyCustomer(customerId, verificationTypeId, reference))
