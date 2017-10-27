from main import *

def lookupProductName(id):
    cursor.execute('''SELECT name FROM Product WHERE productId = ?''', (id,))
    productname = cursor.fetchone()[0]
    return productname

def lookupProductId(productname):
    cursor.execute('''SELECT productId FROM Product WHERE name = ?''', [productname,])
    return cursor.fetchone()[0]

def calculateProductPrice(productid):
    epochTime = str(datetime.date.today())
    cursor.execute('''SELECT EXISTS(SELECT * FROM discount d WHERE d.productid = ? AND d.datetimeStart < ? AND (d.datetimeEnd > ? OR d.datetimeEnd IS NULL))''', (productid, epochTime, epochTime))
    if cursor.fetchone()[0] == 1:
        cursor.execute('''SELECT d.productId, p.value, d.percentage FROM discount d INNER JOIN price p ON p.productId = d.productId WHERE d.productid = ? AND d.datetimeStart < ? AND (d.datetimeEnd > ? OR d.datetimeEnd IS NULL)''',(productid, epochTime, epochTime))
        productDiscount = cursor.fetchone()
        productPrice = productDiscount[1] * productDiscount[2]
        return eval('{:.2f}'.format(productPrice))
    else:
        try:
            cursor.execute('''SELECT p.value FROM price p WHERE p.productid = ? AND p.datetimeStart < ? AND (p.datetimeEnd > ? OR p.datetimeEnd IS NULL)''',(productid, epochTime, epochTime))
            productPrice = cursor.fetchone()
            return productPrice[0]
        except:
            messageBox('Geen product geselecteerd','U heeft geen product geselecteerd. Selecteer een product voordat u deze toe wilt voegen aan te transactie.','error')
            return

def fetchProducts():
    cursor.execute("SELECT pro.name, pri.value, pri.datetimeStart, pri.datetimeEnd FROM product pro INNER JOIN price pri ON pro.productId = pri.productId  WHERE pri.datetimeStart <= datetime('now', 'localtime') AND (pri.datetimeEnd ISNULL OR pri.datetimeEnd > datetime('now', 'localtime'))")
    return cursor.fetchall()

def fetchProductsPerCategory(categories):
    epochTime = str(datetime.date.today())
    products = dict()
    for category in categories:
        cursor.execute('''SELECT productId, name FROM product WHERE datetimeStart < ? AND (datetimeEnd > ? OR datetimeEnd IS NULL) AND categoryId IS ?''',(epochTime, epochTime, category[0]))
        products[category] = cursor.fetchall()
    cursor.execute('''SELECT productId, name FROM product WHERE datetimeStart < ? AND (datetimeEnd > ? OR datetimeEnd IS NULL) AND categoryId IS NULL''',(epochTime, epochTime))
    return products

def addProduct(productName, productDatetimeStart, priceValue, priceDatetimeStart, productDatetimeEnd=None, priceDatetimeEnd=None):
    'Takes a name, startdate, price and optionally an enddate. This function creates the new product and prices it.'
    cursor.execute(''' INSERT INTO product(name,datetimeStart) VALUES(?,?)''', [productName, productDatetimeStart])
    cursor.execute('''SELECT productId FROM product WHERE name = ?''', [productName,])
    id = cursor.lastrowid
    cursor.execute(''' INSERT INTO price( productId, datetimeStart, value) VALUES(?,?,?)''', [id, priceDatetimeStart,priceValue])
    if productDatetimeEnd != None: # If Enddate was specified, add Enddate to database
        cursor.execute('''UPDATE product SET datetimeEnd = ? WHERE name = ?''', [productDatetimeEnd, productName])
    if priceDatetimeEnd != None:
        cursor.execute('''UPDATE price SET datetimeEnd = ? WHERE productId = ?''', [priceDatetimeEnd, id])
    conn.commit()

def setProductDatetimeEnd(productId, productDatetimeEnd):
    cursor.execute('''UPDATE product SET datetimeEnd = ? WHERE productId = ?''', [productDatetimeEnd,productId])
    cursor.execute('''UPDATE price SET datetimeEnd = ? WHERE productId = ?''', [productDatetimeEnd,productId])
    conn.commit()

def setNewProductPrice(productId, price, newPriceDatetimeStart, newPriceDatetimeEnd):
    if newPriceDatetimeEnd == '':
        newPriceDatetimeEnd = None
    cursor.execute('''UPDATE price SET datetimeEnd = ? WHERE productId = ?''', [newPriceDatetimeStart, productId])
    cursor.execute('''INSERT INTO price(productId,value,datetimeStart,datetimeEnd)''', [productId, price, newPriceDatetimeStart,newPriceDatetimeEnd])

