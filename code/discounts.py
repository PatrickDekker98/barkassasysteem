from main import *

def fetchDiscounts():
    cursor.execute("SELECT pro.name, pri.value, dis.percentage, dis.datetimeStart, dis.datetimeEnd FROM product pro INNER JOIN price pri ON pro.productId = pri.productId INNER JOIN discount dis ON pro.productId = dis.productId WHERE pri.datetimeStart <= datetime('now', 'localtime') AND (pri.datetimeEnd ISNULL OR pri.datetimeEnd > datetime('now', 'localtime'))")
    return cursor.fetchall()