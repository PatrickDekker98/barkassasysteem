import sqlite3, time, guiNumpad as numpad, calculateTransaction as calcT, tkinter, guiProducts

db = sqlite3.connect('../barkassasysteem.db')
cur = db.cursor()

def addTransaction():
    transaction = []
    total = 0
    done = False
    while done == False:
        choice = guiProducts.call()
        if choice == 'End':
            done = True
            continue
        elif choice != '':
            transaction.append(addProduct(choice))
        else:
            print("")
    totalPrice = 0
    for product in transaction:
        product.append(calcT.calculateProductPrice(product[0]))
        totalPrice += (int(product[1]) * float(product[2]))
    print('{:10} {:7} {:5}'.format('Product', 'Aantal', 'Prijs'))
    for product in transaction:
        print('{:10} {:7} €{:5.2f}'.format(lookupProductName(product[0])[:10],(str(product[1]) + 'x'),(int(product[1])*float(product[2]))))
    print('_________________________')
    print('{:19}€{:.2f}'.format('',totalPrice))


    #Coupon check HIER
    #Authenticatie en verificatie
    verificationmethodId = 1
    epochTime = int(str(time.time()).split('.')[0] + str(time.time()).split('.')[1][:3])
    cur.execute('''INSERT INTO 'transaction' (datetime, verificationMethodId) VALUES (?, ?)''',(epochTime,verificationmethodId))
    db.commit()
    cur.execute('''SELECT transactionId from 'transaction' WHERE datetime = ?''', (epochTime,))
    transactionId = cur.fetchone()[0]
    for product in transaction:
        cur.execute('''INSERT INTO purchase(transactionId,productId,amount) VALUES(?,?,?)''',(transactionId,product[0],product[1]))
    #Transactie geslaagd
    db.commit()

def addProduct(id):
    productName = lookupProductName(id)
    amount = numpad.call(productName)
    return [id, amount]

def lookupProductName(id):
    cur.execute('''SELECT name FROM Product WHERE productId = ?''', (id,))
    productname = cur.fetchone()[0]
    return productname

addTransaction()

db.close()