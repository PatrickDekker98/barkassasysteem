from main import *

def fetchDiscounts():
    cursor.execute("SELECT pro.name, pri.value, dis.percentage, dis.datetimeStart, dis.datetimeEnd, dis.discountId FROM product pro INNER JOIN price pri ON pro.productId = pri.productId INNER JOIN discount dis ON pro.productId = dis.productId WHERE pri.datetimeStart <= datetime('now', 'localtime') AND (pri.datetimeEnd ISNULL OR pri.datetimeEnd > datetime('now', 'localtime'))")
    return cursor.fetchall()

def addDiscount(productId, discountPercentage, discountDatetimeStart, discountDatetimeEnd):
    if discountDatetimeEnd == '':
        discountDatetimeEnd = None
    cursor.execute(''' SELECT EXISTS(SELECT * FROM discount WHERE productId = ? AND datetimeStart <= ? AND (datetimeEnd ISNULL OR datetimeEnd >= ?))''', [productId, discountDatetimeStart, discountDatetimeEnd])
    if cursor.fetchall == 1:
        if tkinter.messagebox.askyesno("Bestaande korting gevonden!", "Binnen de door u aangeven periode, is voor dit product al een korting actief. Wilt u deze korting beeïndigen?"):
            cursor.execute('''UPDATE discount SET datetimeEnd = ? WHERE discountId = (SELECT discountId FROM discount WHERE productId = ? AND datetimeStart <= ? AND (datetimeEnd ISNULL OR datetimeEnd >= ?) ''', discountDatetimeStart, productId,discountDatetimeStart,discountDatetimeEnd)
        else:
            return False
    cursor.execute('''INSERT INTO discount(productId, percentage, datetimeStart, datetimeEnd) VALUES(?,?,?,?)''', [productId, discountPercentage, discountDatetimeStart, discountDatetimeEnd ])
    conn.commit()
    return True

def setDiscountEnddate(discountId, discountDateTimeEnd):
    cursor.execute('''UPDATE discount SET datetimeEnd = ? WHERE discountId = ?''', [discountDateTimeEnd,discountId])
    conn.commit()
    return True