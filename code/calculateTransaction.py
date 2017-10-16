import sqlite3, time

db = sqlite3.connect('..\\barkassasysteem.db')
cur = db.cursor()

def calculateTransaction(transaction):
    totalCost = 0
    for product in transaction:
        totalCost += (calculateProductPrice(product[0]) * product[1])
    return totalCost

def calculateProductPrice(productid):
    epochTime = int(str(time.time()).split('.')[0] + str(time.time()).split('.')[1][:3])
    cur.execute('''SELECT EXISTS(SELECT * FROM discount d WHERE d.productid = ? AND d.datetimeStart < ? AND (d.datetimeEnd > ? OR d.datetimeEnd IS NULL))''', (productid, epochTime, epochTime))
    if cur.fetchone()[0] == 1:
        cur.execute('''SELECT d.productId, p.value, d.percentage FROM discount d INNER JOIN price p ON p.productId = d.productId WHERE d.productid = ? AND d.datetimeStart < ? AND (d.datetimeEnd > ? OR d.datetimeEnd IS NULL)''',(productid, epochTime, epochTime))
        productDiscount = cur.fetchone()
        productPrice = productDiscount[1] * productDiscount[2]
        return eval('{:.2f}'.format(productPrice))
    else:
        cur.execute('''SELECT p.value FROM price p WHERE p.productid = ? AND p.datetimeStart < ? AND (p.datetimeEnd > ? OR p.datetimeEnd IS NULL)''',(productid, epochTime, epochTime))
        productPrice = cur.fetchone()
        return (productPrice[0])

#db.close()