import sqlite3

def addProduct(name, startdate, price, enddate=None):
    'Takes a name, startdate, price and optionally an enddate. This function creates the new product and prices it.'
    cursor.execute('''SELECT * FROM product''')
    id = cursor.lastrowid + 1
    cursor.execute(''' INSERT INTO product(productId,name,datetimeStart) VALUES(?,?,?)''', [id, name, startdate])
    cursor.execute(''' INSERT INTO price(productId, datetimeStart, value) VALUES(?,?,?)''', [id, startdate,price])
    if enddate != None: # If Enddate was specified, add Enddate to database
        cursor.execute('''UPDATE product SET datetimeEnd = ? WHERE productId = ?''', [enddate, id])
        cursor.execute('''UPDATE price SET datetimeEnd = ? WHERE productId = ?''', [enddate, id])
    db.commit()

def deactivateProduct(naam, enddate):
    'Takes a name and a date. This function deactivates the '
    cursor.execute('''SELECT productid FROM Product WHERE name = ?''', [naam])
    id = cursor.fetchone()[0]
    cursor.execute('''UPDATE Price SET datetimeEnd = ? WHERE productId = ?''', (enddate, id))
    db.commit()

def alterPrice(name, newprice):
    cursor.execute('''SELECT productId FROM product WHERE name = ?''', [name])
    id = cursor.fetchone()[0]
    cursor.execute(''' UPDATE price SET value = ? WHERE productId = ?''', (newprice, id))
    db.commit()

#Tijdelijke database in geheugen aanmaken
db = sqlite3.connect(':memory:')
cursor = db.cursor()

#Database tabellen maken
cursor.execute('''CREATE TABLE product(productId INTEGER PRIMARY KEY, name TEXT, datetimeStart DATETIME, datetimeEnd DATETIME)''')
cursor.execute('''CREATE TABLE price(productId INTEGER , datetimeStart DATETIME, datetimeEnd DATETIME, value DECIMAL, FOREIGN KEY(productId) REFERENCES product(productId), PRIMARY KEY (productId, datetimeStart))''')
db.commit()

#Dummy data invoeren
addProduct(name='Bier', startdate='04-10-2017', price=1.20)
addProduct(name='Cola', startdate='05-10-2017', price=1.00)
addProduct(name='Fanta', startdate='04-10-2017', price=1.20)
addProduct(name='7-up', startdate='05-10-2017', price=1.00)
deactivateProduct('Bier', '20-10-2017')
alterPrice('Cola', 1.95)

#cursor.execute('''SELECT * FROM Product''')
#for row in cursor:
#    print(row)

#cursor.execute('''SELECT * FROM Prijs''')
#for row in cursor:
#    print(row)

cursor.execute('''SELECT name, value, product.datetimeStart, product.datetimeEnd FROM Product INNER JOIN price ON Product.productId = price.productId''')
print('{:15} {:10} {:15} {:10}'.format('Productnaam', 'Prijs', 'Start datum', 'Eind datum'))
for row in cursor:
    print('{:15} {:<10.2f} {:15} {:10}'.format(row[0], row[1], row[2], str(row[3])))

db.close()