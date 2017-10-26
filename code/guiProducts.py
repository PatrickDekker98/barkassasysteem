from main import *
import products, discounts

class productMain:
    def __init__(self, master):
        self.master = master

        self.contentFrame = tkinter.Frame(self.master)
        returnFrame = tkinter.Frame(self.master)


        self.buildMenu = self.buildMenuFrame(self.contentFrame)

        self.returnFrame = self.buildReturn(returnFrame)

        self.contentFrame.pack(side='top')
        returnFrame.pack(side='left')


    def buildMenuFrame(self, master):
        self.resetContent()

        productsMenuFrame = tkinter.Frame(master)
        discountsMenuFrame = tkinter.Frame(master)


        tkinter.Button(productsMenuFrame, text='Producten', font=('Arial', 15), height=2, width=15, bg='lightblue', command=self.viewProduct).pack()
        tkinter.Button(discountsMenuFrame, text='Kortingen', font=('Arial', 15), height=2, width=15, bg='lightblue', command=self.viewDiscount).pack()

        productsMenuFrame.grid(column=0,row=0)
        discountsMenuFrame.grid(column=1,row=0)

    def viewProduct(self):
        self.resetContent()

        tkinter.Label(self.contentFrame, text='{:83}{:21}{:36}{:12}'.format('Product', 'Prijs', 'Start', 'Eind')).grid(column=0,row=0, sticky='w', columnspan=4)
        self.productsListbox = tkinter.Listbox(self.contentFrame, font='consolas', width=200)
        self.productsListbox.grid(column=0,row=1, columnspan=4)
        currentProducts = products.fetchProducts()
        for p in currentProducts:
            item = '{:30}{:<8.2f}{:13}{:20}'.format(str(p[0]), p[1], str(p[2])[:10], str(p[3]))
            self.productsListbox.insert('end', item)
        tkinter.Button(self.contentFrame, font=('Arial', 20), height=1, width=10, text='Toevoegen', bg='lightgreen', command=self.addProduct).grid(column=2,row=2)
        tkinter.Button(self.contentFrame, font=('Arial', 20), height=1, width=10, text='Aanpassen', bg='yellow', command=self.alterProduct).grid(column=3,row=2)


    def addProduct(self):
        self.resetContent()
        productInputFrame = tkinter.Frame(self.contentFrame)
        priceInputFrame = tkinter.Frame(self.contentFrame)

        productInputFrame.pack(side='left')
        priceInputFrame.pack(side='left')

        tkinter.Label(productInputFrame, text="Product:", font=('Arial', 20)).grid(column=0,row=0,columnspan=3, sticky='w')
        tkinter.Label(productInputFrame, text='Naam').grid(column=0, row=1, sticky='w')
        tkinter.Label(productInputFrame, text='Beschikbaar vanaf').grid(column=0, row=2, sticky='w')
        tkinter.Label(productInputFrame, text='Beschikbaar tot').grid(column=0, row=3, sticky='w')
        productInputFrame.columnconfigure(3,minsize=50)

        self.productNameEntry = tkinter.Entry(productInputFrame)
        self.productDatetimeStartEntry = tkinter.Entry(productInputFrame)
        self.productDatetimeEndEntry = tkinter.Entry(productInputFrame)
        self.productNameEntry.grid(column=1, row=1)
        self.productDatetimeStartEntry.grid(column=1,row=2)
        self.productDatetimeEndEntry.grid(column=1,row=3)

        tkinter.Button(productInputFrame, text='Vandaag', command=lambda: self.currentDate(self.productDatetimeStartEntry)).grid(column=2,row=2)
        tkinter.Button(priceInputFrame, text='Vandaag', command=lambda: self.currentDate(self.priceDatetimeStartEntry)).grid(column=2, row=2)

        tkinter.Label(priceInputFrame, text="Prijs:", font=('Arial', 20)).grid(column=0, row=0, columnspan=3, sticky='w')
        tkinter.Label(priceInputFrame, text='Prijs').grid(column=0, row=1, sticky='w')
        tkinter.Label(priceInputFrame, text='Van').grid(column=0, row=2, sticky='w')
        tkinter.Label(priceInputFrame, text='Tot').grid(column=0, row=3, sticky='w')
        priceInputFrame.columnconfigure(3, minsize=50)

        self.priceValueEntry = tkinter.Entry(priceInputFrame)
        self.priceDatetimeStartEntry = tkinter.Entry(priceInputFrame)
        self.priceDatetimeEndEntry = tkinter.Entry(priceInputFrame)
        self.priceValueEntry.grid(column=1, row=1)
        self.priceDatetimeStartEntry.grid(column=1, row=2)
        self.priceDatetimeEndEntry.grid(column=1, row=3)

        tkinter.Button(self.contentFrame, text='Voeg Toe', bg='lightgreen', command=self.addProductFinish).pack(side='bottom')

    def addProductFinish(self):
        if self.productNameEntry.get() == '':
            tkinter.messagebox.showwarning("Ongelidge invoer!","Voer een productnaam in!")
            return
        elif self.productDatetimeStartEntry.get() == '':
            tkinter.messagebox.showwarning("Ongelidge invoer!", "Voer een startdatum voor het product in!")
            return
        elif self.priceValueEntry.get() == '':
            tkinter.messagebox.showwarning("Ongelidge invoer!", "Voer een prijs in!")
            return
        elif self.priceDatetimeStartEntry.get() == '':
            tkinter.messagebox.showwarning("Ongelidge invoer!", "Voer een startdatum voor de prijs in!")
            return
        products.addProduct(self.productNameEntry.get(), self.productDatetimeStartEntry.get(), self.priceValueEntry.get(), self.priceDatetimeStartEntry.get())
        self.viewProduct()

    def alterProduct(self):
        productId = (self.productsListbox.index('active') + 1)
        self.resetContent()

        productInputFrame = tkinter.Frame(self.contentFrame)
        priceInputFrame = tkinter.Frame(self.contentFrame)

        productInputFrame.grid(column=0,row=0,sticky='n')
        priceInputFrame.grid(column=1,row=0,sticky='n')

        tkinter.Label(productInputFrame, text="Product:", font=('Arial', 20)).grid(column=0, row=0, columnspan=3, sticky='w')

        tkinter.Label(productInputFrame, text='Beschikbaar tot').grid(column=0, row=1, sticky='w')
        productInputFrame.columnconfigure(3, minsize=50)


        self.productDatetimeEndEntry = tkinter.Entry(productInputFrame)
        self.productDatetimeEndEntry.grid(column=1, row=1)

        tkinter.Button(productInputFrame, text='Vandaag', command=lambda: self.currentDate(self.productDatetimeEndEntry)).grid(column=2, row=1)
        tkinter.Button(priceInputFrame, text='Vandaag', command=lambda: self.currentDate(self.priceDatetimeStartEntry)).grid(column=2, row=2)

        tkinter.Label(priceInputFrame, text="Prijs:", font=('Arial', 20)).grid(column=0, row=0, columnspan=3, sticky='w')
        tkinter.Label(priceInputFrame, text='Nieuwe prijs').grid(column=0, row=1, sticky='w')
        tkinter.Label(priceInputFrame, text='Van').grid(column=0, row=2, sticky='w')
        tkinter.Label(priceInputFrame, text='Tot').grid(column=0, row=3, sticky='w')
        priceInputFrame.columnconfigure(3, minsize=50)

        self.priceValueEntry = tkinter.Entry(priceInputFrame)
        self.priceDatetimeStartEntry = tkinter.Entry(priceInputFrame)
        self.priceDatetimeEndEntry = tkinter.Entry(priceInputFrame)
        self.priceValueEntry.grid(column=1, row=1)
        self.priceDatetimeStartEntry.grid(column=1, row=2)
        self.priceDatetimeEndEntry.grid(column=1, row=3)

        tkinter.Button(self.contentFrame, text='Pas aan', bg='lightgreen', command=lambda: self.alterProductFinish(productId)).grid(column=2,row=0,sticky='s')

    def alterProductFinish(self, productId):
        if self.productDatetimeEndEntry.get() == '' and self.priceValueEntry.get() == '' and self.priceDatetimeStartEntry.get() == '':
            tkinter.messagebox.showwarning("Ongeldige invoer!", "Vul iets in om aan te passen!")
            return
        else:
            if self.productDatetimeEndEntry.get() != '':
                products.setProductDatetimeEnd(productId, self.productDatetimeEndEntry.get())
            elif self.priceValueEntry.get() != '' and self.priceDatetimeStartEntry.get() != '':
                products.setNewProductPrice(productId, self.priceValueEntry.get(), self.priceDatetimeStartEntry.get(),self.priceDatetimeEndEntry.get())
                return
            elif (self.priceValueEntry.get() == '' or self.priceDatetimeStartEntry.get() == '') :
                tkinter.messagebox.showwarning("Ongeldige invoer!", "U kunt geen nieuwe prijs instellen, zonder een startdatum in te voeren, of andersom!")
                return
        self.viewProduct()
    def viewDiscount(self):
        self.resetContent()

        tkinter.Label(self.contentFrame, text='{:83}{:21}{:36}{:12}'.format('Product', 'Prijs', 'Start', 'Eind')).grid(column=0,row=0, sticky='w')
        productsListbox = tkinter.Listbox(self.contentFrame, font='consolas', width=200)
        productsListbox.grid(column=0,row=1, columnspan=4)
        currentProducts = discounts.fetchDiscounts()
        for p in currentProducts:
            item = '{:30}{:<8.2f}{:13}{:20}'.format(str(p[0]), p[1], str(p[2])[:10], str(p[3]))
            productsListbox.insert('end', item)
        tkinter.Button(self.contentFrame, font=('Arial', 20), height=1, width=10, text='Toevoegen', bg='lightgreen', command=self.addDiscount).grid(column=2, row=2)
        tkinter.Button(self.contentFrame, font=('Arial', 20), height=1, width=10, text='Aanpassen', bg='yellow',command=self.alterDiscount).grid(column=3, row=2)


    def addDiscount(self):
        self.resetContent()



    def alterDiscount(self):
        self.resetContent()



    def resetContent(self):
        for widget in self.contentFrame.winfo_children():
            widget.destroy()

    def buildReturn(self, master):
        tkinter.Button(master,text='terug', font=('Arial', 10), command=self.returnFunction).pack(side='left')

    def returnFunction(self):
        self.buildMenu

    def currentDate(self, inputfield):
        inputfield.insert('end', str(datetime.datetime.today())[:19])


if __name__ == "__main__":
    root = tkinter.Tk()
    my_gui = productMain(root)
    root.mainloop()