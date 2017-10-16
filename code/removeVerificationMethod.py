from main import *


def removeVerificationMethod(verificationMethodId):
    try:
        cursor.execute("UPDATE verificationMethod SET datetimeEnd = (datetime('now','localtime')) WHERE verificationMethodId = ?", (verificationMethodId,))
        conn.commit()
        printGui("Verification method succesfully removed!")
        return cursor.rowcount == 1
    except:
        raise ValueError("Verification method could not be removed from the database. Please try again.")


print(removeVerificationMethod(1))
print(removeVerificationMethod(6))
