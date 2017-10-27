from main import *

def lookupProductName(id):
    print(id)
    cursor.execute('''SELECT name FROM Product WHERE productId = ?''', (id,))
    return cursor.fetchone()[0]

def lookupProductId(productname):
    cursor.execute('''SELECT productId FROM Product WHERE name = ?''', [productname,])
    return cursor.fetchone()[0]

def calculateProductPrice(productid):
    cursor.execute('''SELECT EXISTS(SELECT * FROM discount WHERE productid = ? AND datetimeStart <= datetime('now', 'localtime') AND (datetimeEnd >= datetime('now', 'localtime') OR datetimeEnd IS NULL))''', (productid,))
    if cursor.fetchone()[0] == 1:
        cursor.execute('''SELECT d.productId, p.value, d.percentage FROM discount d INNER JOIN price p ON p.productId = d.productId WHERE d.productid = ? AND d.datetimeStart <= datetime('now', 'localtime') AND (d.datetimeEnd >= datetime('now', 'localtime') OR d.datetimeEnd IS NULL)''',(productid, ))
        productDiscount = cursor.fetchone()
        productPrice = productDiscount[1] * productDiscount[2]
        return eval('{:.2f}'.format(productPrice))
    else:
        cursor.execute('''SELECT value FROM price WHERE productId = ? AND datetimeStart <= datetime('now', 'localtime') AND (datetimeEnd >= datetime('now', 'localtime') OR datetimeEnd IS NULL)''',(productid, ))
        productPrice = cursor.fetchone()
        return productPrice[0]

def fetchProducts():
    cursor.execute("SELECT pro.name, pri.value, pri.datetimeStart, pri.datetimeEnd FROM product pro INNER JOIN price pri ON pro.productId = pri.productId  WHERE pri.datetimeStart <= datetime('now', 'localtime') AND (pri.datetimeEnd ISNULL OR pri.datetimeEnd > datetime('now', 'localtime'))")
    return cursor.fetchall()

def fetchProductsPerCategory(categories):
    products = dict()
    for category in categories:
        cursor.execute('''SELECT productId, name FROM product WHERE datetimeStart <= datetime('now', 'localtime') AND (datetimeEnd >= datetime('now', 'localtime') OR datetimeEnd IS NULL) AND categoryId IS ?''',[category[0]])
        products[category] = cursor.fetchall()
    return products

def addProduct(productName, productDatetimeStart, priceValue, priceDatetimeStart, categoryId, productDatetimeEnd=None, priceDatetimeEnd=None):
    'Takes a name, startdate, price and optionally an enddate. This function creates the new product and prices it.'
    print(categoryId)
    cursor.execute(''' INSERT INTO product(name,datetimeStart, categoryId) VALUES(?,?,?)''', [productName, productDatetimeStart, categoryId])
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
    cursor.execute('''INSERT INTO price(productId,value,datetimeStart,datetimeEnd) VALUES(?,?,?,?)''', [productId, price, newPriceDatetimeStart,newPriceDatetimeEnd])
    conn.commit()

def lookupProductCategory(productId):
    cursor.execute('''SELECT categoryId FROM product WHERE productId = ?''', [productId])
    return cursor.fetchone()[0]

def setNewProductCategory(productId, categoryId):
    cursor.execute('''UPDATE product SET categoryId = ? WHERE productId = ?''', [categoryId, productId])
    conn.commit()
    return