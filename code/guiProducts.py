from main import *
import products, discounts, categories, telegramSend

class productMain:
    def __init__(self, master):
        self.master = master

        self.contentFrame = tkinter.Frame(self.master)

        self.buildMenu = self.buildMenuFrame(self.contentFrame)

        self.contentFrame.pack(side='top')


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

        tkinter.Label(self.contentFrame, text='{:103}{:30}{:44}{:12}'.format('Product', 'Prijs', 'Start', 'Eind')).grid(column=0,row=0, sticky='w', columnspan=4)
        self.productsListbox = tkinter.Listbox(self.contentFrame, font='consolas', width=200)
        self.productsListbox.grid(column=0,row=1, columnspan=4)
        currentProducts = products.fetchProducts()
        for p in currentProducts:
            item = '{:30}€{:<8.2f}{:13}{:20}'.format(str(p[0]), p[1], str(p[2])[:10], str(p[3])[:10])
            self.productsListbox.insert('end', item)
        tkinter.Button(self.contentFrame, font=('Arial', 20), height=1, width=10, text='Toevoegen', bg='lightgreen', command=self.addProduct).grid(column=1,row=2)
        tkinter.Button(self.contentFrame, font=('Arial', 20), height=1, width=10, text='Aanpassen', bg='yellow', command=self.alterProduct).grid(column=2,row=2)


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
        tkinter.Label(productInputFrame, text='Categorie').grid(column=0, row=4, sticky='w')
        productInputFrame.columnconfigure(3,minsize=50)

        self.categoryList = []
        for product in categories.getCategories():
            self.categoryList.append(product[1])
        self.selectedCategory = tkinter.StringVar()
        self.selectedCategory.set(self.categoryList[0])
        self.selectedCategoryId = categories.getCategory(self.selectedCategory.get()[0])

        self.productSelection = tkinter.OptionMenu(productInputFrame, self.selectedCategory, *self.categoryList, command=self.setSelectedCategory)
        self.productSelection.grid(column=1, row=4)

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


    def setSelectedCategory(self, value):
        self.selectedCategory = value
        self.selectedCategoryId = categories.getCategoryId(value)


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

        productName = self.productNameEntry.get()
        productDateTimeStart = self.productDatetimeStartEntry.get()
        productPrice = self.priceValueEntry.get()
        productDateTimeEnd = self.priceDatetimeEndEntry.get()
        productCategoryId = self.selectedCategoryId
        products.addProduct(productName, productDateTimeStart, productPrice, productDateTimeEnd, productCategoryId)
#        products.addProduct(self.productNameEntry.get(), self.productDatetimeStartEntry.get(), self.priceValueEntry.get(), self.priceDatetimeStartEntry.get(), self.selectedCategoryId)
        telegramMsg = 'Beste klant we hebben een nieuw product; ' + productName + ' vanaf ' + productDateTimeStart + ' zal dit product beschikbaar zijn'
        telegramSend.sendToAll(telegramMsg)
        self.viewProduct()

    def alterProduct(self):
        productId = self.productsListbox.index('active') + 1
        self.resetContent()

        productInputFrame = tkinter.Frame(self.contentFrame)
        priceInputFrame = tkinter.Frame(self.contentFrame)

        productInputFrame.grid(column=0,row=0,sticky='n')
        priceInputFrame.grid(column=1,row=0,sticky='n')


        tkinter.Label(productInputFrame, text=("Product:  " + products.lookupProductName(productId)), font=('Arial', 20)).grid(column=0, row=0, columnspan=1, sticky='w')
        tkinter.Label(productInputFrame, text='Beschikbaar tot').grid(column=0, row=1, sticky='w')
        tkinter.Label(productInputFrame, text='Nieuwe categorie').grid(column=0, row=2, sticky='w')
        productInputFrame.columnconfigure(3, minsize=50)

        self.categoryList = []
        for product in categories.getCategories():
            self.categoryList.append(product[1])
            if product[0] == products.lookupProductCategory(productId):
                self.selectedCategory = tkinter.StringVar()
                self.selectedCategory.set(product[1])
                self.selectedCategoryId = categories.getCategory(self.selectedCategory.get()[0])

        self.productSelection = tkinter.OptionMenu(productInputFrame, self.selectedCategory, *self.categoryList, command=self.setSelectedCategory)
        self.productSelection.grid(column=1, row=2)

        self.productDatetimeEndEntry = tkinter.Entry(productInputFrame)
        self.productDatetimeEndEntry.grid(column=1, row=1)

        tkinter.Button(productInputFrame, text='Vandaag', command=lambda: self.currentDate(self.productDatetimeEndEntry)).grid(column=2, row=1)
        tkinter.Button(priceInputFrame, text='Vandaag', command=lambda: self.currentDate(self.priceDatetimeStartEntry)).grid(column=2, row=2)

        tkinter.Label(priceInputFrame, text=("Prijs:  " + str(products.calculateProductPriceWODiscount(productId))), font=('Arial', 20)).grid(column=0, row=0, columnspan=3, sticky='w')
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
        if self.productDatetimeEndEntry.get() == '' and self.priceValueEntry.get() == '' and self.priceDatetimeStartEntry.get() == '' and self.selectedCategoryId == products.lookupProductCategory(productId):
            tkinter.messagebox.showwarning("Ongeldige invoer!", "Vul iets in om aan te passen!")
            return

        if self.productDatetimeEndEntry.get() != '':
            products.setProductDatetimeEnd(productId, self.productDatetimeEndEntry.get())

        if self.priceValueEntry.get() != '':
                if self.priceDatetimeStartEntry.get() != '':
                    products.setNewProductPrice(productId, self.priceValueEntry.get(), self.priceDatetimeStartEntry.get(),self.priceDatetimeEndEntry.get())
                else:
                    tkinter.messagebox.showwarning("Ongeldige invoer!", "Om de prijs aan te passen, dient u ook een startdatum in te voeren!")
                return

        if self.priceDatetimeStartEntry.get() != '':
                if self.priceValueEntry.get() != '':
                    None
                else:
                    tkinter.messagebox.showwarning("Ongeldige invoer!", "U heeft de startdatum voor een nieuwe prijs ingegeven, zonder een waarde in te geven voor deze nieuwe prijs!")
                return

        if self.selectedCategoryId != products.lookupProductCategory(productId):
            products.setNewProductCategory(productId,self.selectedCategoryId)

        self.viewProduct()


    def viewDiscount(self):
        self.resetContent()

        tkinter.Label(self.contentFrame, text='{:103}{:30}{:30}{:32}{:45}{:28}'.format('Product', 'Prijs', 'Korting', 'Nieuwe prijs', 'Startdatum', 'Einddatum')).grid(column=0,row=0, sticky='w', columnspan=4)
        discountsListbox = tkinter.Listbox(self.contentFrame, font='consolas', width=200)
        discountsListbox.grid(column=0,row=1, columnspan=4)
        currentDiscounts = discounts.fetchDiscounts()
        for d in currentDiscounts:
            item = '{:30}€{:<8.2f}{:10}€{:<10.2f}{:15}{:}'.format(str(d[0]), d[1], str(str(d[2]*100)+'%'), (d[1]*d[2]), str(d[3])[:10], str(d[4])[:10])
            discountsListbox.insert('end', item)
        tkinter.Button(self.contentFrame, font=('Arial', 20), height=1, width=10, text='Toevoegen', bg='lightgreen', command=self.addDiscount).grid(column=1, row=2)
        tkinter.Button(self.contentFrame, font=('Arial', 20), height=1, width=10, text='Aanpassen', bg='yellow',command=lambda: self.alterDiscount(currentDiscounts[discountsListbox.index('active')][5])).grid(column=2, row=2)


    def addDiscount(self):
        self.resetContent()
        productInputFrame = tkinter.Frame(self.contentFrame)
        discountInputFrame = tkinter.Frame(self.contentFrame)

        productInputFrame.grid(column=0,row=0,sticky='nw')
        discountInputFrame.grid(column=1,row=0,sticky='ne')

        tkinter.Label(productInputFrame, text="Product:", font=('Arial', 20)).grid(column=0, row=0, columnspan=3,sticky='nw')
        tkinter.Label(productInputFrame, text='Naam').grid(column=0, row=1, sticky='w')
        productInputFrame.columnconfigure(3, minsize=50)

        productsList = []
        for product in products.fetchProducts():
            productsList.append(product[0])
        self.selectedProduct = tkinter.StringVar()
        self.selectedProduct.set(productsList[0])
        self.selectedProductId = products.lookupProductId(self.selectedProduct.get())

        self.productSelection = tkinter.OptionMenu(productInputFrame, self.selectedProduct, *productsList, command=self.setSelectedProduct)
        self.productSelection.grid(column=1, row=1)

        tkinter.Button(discountInputFrame, text='Vandaag', command=lambda: self.currentDate(self.discountDatetimeStartEntry)).grid(column=2, row=2)

        tkinter.Label(discountInputFrame, text="Korting:", font=('Arial', 20)).grid(column=0, row=0, columnspan=3,sticky='w')
        tkinter.Label(discountInputFrame, text='Percentage').grid(column=0, row=1, sticky='w')
        tkinter.Label(discountInputFrame, text='Van').grid(column=0, row=2, sticky='w')
        tkinter.Label(discountInputFrame, text='Tot').grid(column=0, row=3, sticky='w')
        discountInputFrame.columnconfigure(3, minsize=50)

        self.discountValueEntry = tkinter.Entry(discountInputFrame)
        self.discountDatetimeStartEntry = tkinter.Entry(discountInputFrame)
        self.discountDatetimeEndEntry = tkinter.Entry(discountInputFrame)
        self.discountValueEntry.grid(column=1, row=1)
        self.discountDatetimeStartEntry.grid(column=1, row=2)
        self.discountDatetimeEndEntry.grid(column=1, row=3)

        tkinter.Button(self.contentFrame, text='Voeg Toe', bg='lightgreen', command=self.addDiscountFinish).grid(column=2,row=0,sticky='s')

    def setSelectedProduct(self, value):
        self.selectedProduct = value
        self.selectedProductId = products.lookupProductId(self.selectedProduct)

    def addDiscountFinish(self):
        if int(self.discountValueEntry.get()) > 1:
            discountValue = int(self.discountValueEntry.get()) / 100
        elif self.discountValueEntry.get() < 1:
            discountValue = self.discountValueEntry.get()

        if self.discountValueEntry.get() == '' or self.discountDatetimeStartEntry.get() == '':
            tkinter.messagebox.showwarning("Ongeldige invoer!", "Zorg dat minimaal het percentage en de startdatum ingevuld zijn!")
            return
        else:
            discounts.addDiscount(self.selectedProductId, discountValue, self.discountDatetimeStartEntry.get(), self.discountDatetimeEndEntry.get())
        self.viewDiscount()

    def alterDiscount(self , discountId):
        self.resetContent()

        discountInputFrame = tkinter.Frame(self.contentFrame)

        discountInputFrame.grid(column=0, row=0, sticky='n')

        discountDatetimeEndEntry = tkinter.Entry(discountInputFrame)
        discountDatetimeEndEntry.grid(column=1,row=1,sticky='w')
        tkinter.Button(discountInputFrame, text='Vandaag', command=lambda: self.currentDate(discountDatetimeEndEntry)).grid(column=2, row=1)

        tkinter.Label(discountInputFrame, text="Korting:", font=('Arial', 20)).grid(column=0, row=0, columnspan=3,sticky='w')
        tkinter.Label(discountInputFrame, text='Eindigt op').grid(column=0, row=1, sticky='w')
        discountInputFrame.columnconfigure(3, minsize=50)

        print(discountId)
        tkinter.Button(self.contentFrame, text='Pas aan', bg='lightgreen', command=lambda: self.alterDiscountFinish(discountId, discountDatetimeEndEntry.get())).grid(column=1, row=0, sticky='s')

    def alterDiscountFinish(self,discountId, datetimeEnd):
        discounts.setDiscountEnddate(discountId, datetimeEnd)
        self.viewDiscount()

    def resetContent(self):
        for widget in self.contentFrame.winfo_children():
            widget.destroy()


    def currentDate(self, inputfield):
        inputfield.insert('end', str(datetime.datetime.today())[:19])


if __name__ == "__main__":
    root = tkinter.Tk()
    my_gui = productMain(root)
    root.mainloop()
