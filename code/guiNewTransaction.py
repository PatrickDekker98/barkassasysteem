from main import *
import sqlite3,datetime,guiProducts
import tkinter


class productSelection(tkinter.Frame):
    def __init__(self,master):
        self.master=master
        tkinter.Label(self.master, text="Geselecteerd:", font=('Arial', 20), height=2).grid(column=0,row=0)
        self.selection = tkinter.Label(self.master, text="", font=("Arial", 20), height=2)
        self.selection.grid(column=1,row=0, columnspan=2)
        r = 1
        c = 0
        for product in self.fetchProducts():
            cmd = lambda id=product[0]: self.set(id)
            tkinter.Button(self.master, text=product[1][:13], font=('Arial', 15), height=2, width=15, command=cmd).grid(row=r, column=c)
            c += 1
            if c > 2:
                c = 0
                r += 1


    def set(self,productid):
        productname = lookupProductName(productid)
        self.currentSelection = productid
        self.selection.config(text=productname)


    def fetchProducts(self):
        epochTime = str(datetime.date.today())
        cursor.execute(
            '''SELECT productId, name FROM product WHERE datetimeStart < ? AND (datetimeEnd > ? OR datetimeEnd IS NULL)''',
            (epochTime, epochTime))
        products = cursor.fetchall()
        return products


    def returnValue(self):
        value = self.currentSelection
        self.currentSelection = None
        self.selection.config(text='')
        return value


class transactionOverview(tkinter.Frame):
    transaction = []
    total = 0

    def __init__(self,master):
        self.master = master
        self.overview = tkinter.Listbox(self.master, width=55)
        self.overview.grid(column=0, row=1, columnspan=4)
        tkinter.Label(self.master, text="{:20}     {:3}     {:7}".format('Product', 'Aantal', 'Prijs'), font=('Arial', 10)).grid(column=0, row=0,columnspan=2, sticky='w')
        self.totalLabel = tkinter.Label(self.master,text='€ {:.2f}'.format(self.total), font=('Arial', 20), height=1, width=10)
        self.totalLabel.grid(column=1, row=2)
        tkinter.Button(self.master, text="+", font=('Arial', 20), height=1, width=10, bg='lightgreen', command=self.addProduct).grid(column=0, row=3)
        tkinter.Button(self.master, text="-", font=('Arial', 20), height=1, width=10, bg='red',command=self.removeProduct).grid(column=1, row=3)
        tkinter.Button(self.master, text="Afrekenen", font=('Arial', 20), height=1, width=20, bg='green',command=self.endTransaction).grid(column=0, row=4,columnspan=2)


    def addProduct(self):
        try:
            product = my_gui.productSelection.returnValue()
        except:
            messageBox('Geen product geselecteerd', 'U heeft geen product geselecteerd. Selecteer een product voordat u deze toe wilt voegen aan te transactie.', 'error')
            return

        try:
            amount = my_gui.numpad.returnValue()
        except:
            messageBox('Geen aantal gekozen', 'U heeft geen aantal aangegeven. Geef aan hoeveelheid aan voordat u dit toe wilt voegen aan de transactie', 'error')
            return

        pricePerItem = calculateProductPrice(product)
        self.transaction.append([product,amount, pricePerItem])
        self.updateTransactionListbox()


    def updateTransactionListbox(self):
        self.overview.delete(0,'end')
        self.calculateTotal()
        for product in self.transaction:
            print(product)
            self.overview.insert('end', '{:<50}x{:<7}€ {:<7.2f}'.format(lookupProductName(product[0]),product[1],(product[1] * product[2])))


    def removeProduct(self):
        productindex = self.overview.index('active')
        del self.transaction[productindex]
        self.updateTransactionListbox()


    def calculateTotal(self):
        self.total = 0
        for product in self.transaction:
            self.total += (product[1] * product[2])
        self.totalLabel.config(text='€ {:.2f}'.format(self.total))

    def endTransaction(self):
        if self.total == 0:
            messageBox('Lege transactie', 'Dit is een lege transactie. Voeg eerst producten toe voordat u wil afrekenen!', 'info')
        else:
            messageBox('Betaling','U bent klaar om te betalen. Het te betalen bedrag is € {:.2f}'.format(self.total))


class numpadClass(tkinter.Frame):
    def __init__(self,master):
        self.master = master
        self.totalValue = ''
        tkinter.Label(self.master, text="Aantal:", font=('Arial', 20), height=5).grid(column=0, row=0)
        self.amount = tkinter.Label(self.master, text=self.totalValue, font=("Arial", 20), height=5)
        self.amount.grid(column=1, row=0)

        self.buttons = ['1', '2', '3','4', '5', '6','7', '8', '9', '0']
        r = 1
        c = 0
        for b in self.buttons:
            cmd = lambda button=b: self.add(button)
            tkinter.Button(self.master, text=b, font=('Arial', 20), height=2, width=7, command=cmd).grid(row=r, column=c)
            c += 1
            if c > 4:
                c = 0
                r += 1
        tkinter.Button(self.master, text='<', font=('Arial', 20), height=2, width=7, bg='red', command=self.backspace).grid(row=1, column=5)
        tkinter.Button(self.master, text='C', font=('Arial', 20), height=2, width=7, bg='red', command=self.clear).grid(row=2, column=5)


    def add(self,number):
        self.totalValue = self.totalValue + number
        self.amount.config(text=self.totalValue)


    def backspace(self):
        self.totalValue = self.totalValue[:-1]
        self.amount.config(text=self.totalValue)


    def clear(self):
        self.totalValue = ''
        self.amount.config(text=self.totalValue)


    def returnValue(self):
        value = self.totalValue
        self.totalValue = ''
        self.amount.config(text=self.totalValue)
        return int(value)


class newTransaction:
    def __init__(self, master):
        self.master = master
        master.wm_attributes('-fullscreen', 'true')

        productSelectionFrame = tkinter.Frame(self.master)
        self.productSelection = productSelection(productSelectionFrame)
        productSelectionFrame.grid(column=0,row=0, columnspan=2)


        numpadFrame = tkinter.Frame(self.master)
        self.numpad = numpadClass(numpadFrame)
        numpadFrame.grid(column=1,row=1,columnspan=2, sticky='E')

        currentTransactionFrame = tkinter.Frame(self.master)
        currentTransaction = transactionOverview(currentTransactionFrame)
        currentTransactionFrame.grid(column=2,row=0, sticky='e')


def lookupProductName(id):
    cursor.execute('''SELECT name FROM Product WHERE productId = ?''', (id,))
    productname = cursor.fetchone()[0]
    return productname


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


db = '../barkassasysteem.db'
conn = sqlite3.connect(db)
cursor = conn.cursor()

root = tkinter.Tk()
my_gui = newTransaction(root)
root.mainloop()