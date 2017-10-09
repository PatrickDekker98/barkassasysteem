import sqlite3

def product_toevoegen(naam, startdatum, prijs, einddatum=None):
    cursor.execute('''SELECT * FROM Product''')
    id = cursor.lastrowid + 1
    cursor.execute(''' INSERT INTO Product(productid,productnaam) VALUES(?,?)''', [id, naam])
    cursor.execute(''' INSERT INTO Prijs(Product_productid, datumStart, waarde) VALUES(?,?,?)''', [id, startdatum,prijs])
    if einddatum != None:
        cursor.execute('''UPDATE users SET datumEind = ? WHERE productid = ?''', [einddatum, id])
    db.commit()

def product_deactiveren(naam, einddatum):
    cursor.execute('''SELECT productid FROM Product WHERE productnaam = ?''', [naam])
    id = cursor.fetchone()[0]
    cursor.execute('''UPDATE Prijs SET datumEind = ? WHERE Product_productid = ?''', (einddatum, id))
    db.commit()

def prijzen_aanpassen(naam, nieuwePrijs):
    cursor.execute('''SELECT productid FROM Product WHERE productnaam = ?''', [naam])
    id = cursor.fetchone()[0]
    cursor.execute(''' UPDATE Prijs SET waarde = ? WHERE Product_productid = ?''', (nieuwePrijs, id))
    db.commit()

#Tijdelijke database in geheugen aanmaken
db = sqlite3.connect(':memory:')
cursor = db.cursor()

#Database tabellen maken
cursor.execute('''CREATE TABLE Product(productid INTEGER PRIMARY KEY, productnaam TEXT)''')
cursor.execute('''CREATE TABLE Prijs(Product_productid INTEGER , datumStart DATETIME, datumEind DATETIME, waarde DECIMAL, FOREIGN KEY(Product_productid) REFERENCES Procuct(productid), PRIMARY KEY (Product_productid, datumStart))''')
db.commit()

#Dummy data invoeren
product_toevoegen(naam='Bier', startdatum='04-10-2017', prijs=1.20)
product_toevoegen(naam='Cola', startdatum='05-10-2017', prijs=1.00)
product_toevoegen(naam='Fanta', startdatum='04-10-2017', prijs=1.20)
product_toevoegen(naam='7-up', startdatum='05-10-2017', prijs=1.00)
product_deactiveren('Bier', '20-10-2017')
prijzen_aanpassen('Cola', 1.95)

#cursor.execute('''SELECT * FROM Product''')
#for row in cursor:
#    print(row)

#cursor.execute('''SELECT * FROM Prijs''')
#for row in cursor:
#    print(row)

cursor.execute('''SELECT productnaam, waarde, datumStart, datumEind FROM Product INNER JOIN Prijs ON Product.productid = Prijs.Product_productid''')
for row in cursor:
    print(row)

db.close()