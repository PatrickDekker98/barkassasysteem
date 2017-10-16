import sqlite3 as sql

db = '../barkassasysteem.db'
conn = sql.connect(db)
cursor = conn.cursor()


def removeVerificationMethod(verificationMethodId):
    try:
        cursor.execute("UPDATE verificationMethod SET datetimeEnd = (datetime('now','localtime')) WHERE verificationMethodId = ?", (verificationMethodId,))
        conn.commit()
        return cursor.rowcount == 1
    except:
        raise ValueError("Verification method could not be removed from the database. Please try again.")


print(removeVerificationMethod(5))
print(removeVerificationMethod(6))
