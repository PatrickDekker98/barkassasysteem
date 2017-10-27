from main import *


def removeVerificationMethod(verificationMethodId):
    'Removes a verifiactionmethod from the database'
    try:
        cursor.execute("UPDATE verificationMethod SET datetimeEnd = (datetime('now','localtime')) WHERE verificationMethodId = ?", (verificationMethodId,))
        conn.commit()
        return cursor.rowcount == 1
    except:
        raise ValueError("Verification method could not be removed from the database. Please try again.")


print(removeVerificationMethod(1))
print(removeVerificationMethod(6))
