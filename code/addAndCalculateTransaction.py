import sqlite3
from time import gmtime,strftime

db = sqlite3.open(':memory:')
cur = db.cursor()

def addProduct(id):
    productName = lookupProductName(id)
    print('Hoeveel {}?'.format(productName))
    amount = numpad()
    return [id, amount]

def createTransaction():
    transaction = []
    total = 0

    done = False
    while done == False:
        # Geef hier een keuze menu met knoppen die refereren aan de verschillende producten
        # De knop geeft variable keuze de waarde van het
        # Er is 1 END knop om de transactie voort te zetten
        keuze = 1
        if keuze == 'End':
            done = True
            continue
        transaction.append(addProduct(keuze))

    print("Product  Aantal  Prijs")
    transaction = calculateTransaction(transaction)
    for product in transaction: #Geeft een overzicht van de aangegeven producten
        total += product[]
        productName = lookupProductName(product[0])
        print('{} {}x {}'.format(productName,product[1], price))
    print("Totaalbedrag: {}".format(total))


    #Coupon check HIER
    #Authenticatie en verificatie

    cur.execute('''INSERT INTO transaction(transactionId, )''')
    cur.execute('''SELECT * FROM transaction''')
    transactionId = cur.lastrowid + 1
    for product in transaction:
        cur.execute('''INSERT INTO purchase(transactionId,productId,amount) VALUES(?,?,?)''', [transactionId, product[0],product[1]])

def calculateTransaction(transaction):
    transactionWithPrices = []
    dateToday = strftime("%d-%m-%Y")
    for product in transaction:
        cur.execute('''SELECT p.name, price.datetimeStart AS datetimeStart, price.datetimeEnd AS datetimeEnd, discount.datetimeStart AS discountStart discount.datetimeEnd AS discountEnd, discount.discountId FROM product p INNER JOIN price ON p.productId = price.productID INNER JOIN discount ON p.productid = discount.productid WHERE productId = ? AND datetimeStart < ? AND datetimeEnd > ?''', (product[0],dateToday,dateToday))
        transactionWithPrices.append()

def lookupProductName(id):
    cur.execute('''SELECT name FROM Product WHERE id = ?''', [id])
    productname = cur.fetchone()[0]
    return productname

def numpad():
    return 9

cur.execute('''CREATE TABLE product(productId INTEGER, name TEXT, PRIMARY KEY(productId))''')
cur.execute('''CREATE TABLE price(productId INTEGER, datetimeStart DATETIME, datetimeEnd DATETIME, value DECIMAL, FOREIGN KEY(productId) REFERENCES Product(productId), PRIMARY KEY (Product_productid, datumStart))''')
cur.execute('''CREATE TABLE purchase(transaction INTEGER, productId INTEGER, amount INTEGER, FOREIGN KEY(productId, transactionId) REFERENCES product(productId) transaction(transactionId)''')
cur.execute('''CREATE TABLE transaction(transactionId INTEGER, verificationMethodId INTEGER,couponId INTEGER, datetime DATETIME)''')
cur.execute('''CREATE TABLE discount(discountId INTEGER, productId INTEGER, percentage INTEGER, datetimeStart DATETIME, datetimeEnd DATETIME, PRIMARY KEY(discountId), FOREIGN KEY(productId) REFERENCES Product(productId))''')
db.commit()

