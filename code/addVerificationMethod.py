import sqlite3 as sql

db = '../barkassasysteem.db'
conn = sql.connect(db)
cursor = conn.cursor()


def addVerificationMethod(customerId, verificationTypeId, reference):
    try:
        cursor.execute('INSERT INTO verificationMethod (customerId, verificationTypeId, reference) VALUES (?,?,?)', (customerId, verificationTypeId, reference))
        conn.commit()
        return cursor.rowcount == 1
    except:
        raise ValueError("Verification method could not be added to the database. Please try again.")


print(addVerificationMethod(1, 1, "8248"))
print(addVerificationMethod(18, 1, 2938))

data = cursor.execute("select * from verificationMethod")
for row in data:
    print(row)