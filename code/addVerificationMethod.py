from main import *


def addVerificationMethod(customerId, verificationTypeId, reference):
    'Adds a verificationmethod for a user to the database, using CustomerId, verificationtypeId, and the reference'
    try:
        cursor.execute('INSERT INTO verificationMethod (customerId, verificationTypeId, reference) VALUES (?,?,?)', (customerId, verificationTypeId, reference))
        conn.commit()
        printGui("Verification method succesfully added!")
        return cursor.rowcount == 1
    except:
        raise ValueError("Verification method could not be added to the database. Please try again.")

