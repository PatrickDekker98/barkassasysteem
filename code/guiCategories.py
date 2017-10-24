from main import *
import categories


class categoriesOverview(tkinter.Frame):
    categories = []
    total = 0

    def __init__(self,master):


        self.master = master
        self.overview = tkinter.Listbox(self.master, width=55)
        self.overview.grid(column=0, row=1, columnspan=4)
        tkinter.Label(self.master, text="{:20}     {:3}".format('ID', 'Naam'), font=('Arial', 10)).grid(column=0, row=0,columnspan=2, sticky='w')
        tkinter.Button(self.master, text="Aanpassen", font=('Arial', 20), height=1, width=10, bg='#5AF', command=self.editCategory).grid(column=0, row=3)
        tkinter.Button(self.master, text="Verwijderen", font=('Arial', 20), height=1, width=10, bg='#F88',command=self.deleteCategory).grid(column=1, row=3)
        tkinter.Button(self.master, text="Nieuwe categorie", font=('Arial', 20), height=1, width=20, bg='#8F8',command=self.addCategory).grid(column=0, row=4,columnspan=2)
        data = categories.getCategories()
        for row in data:
            self.categories.append(row)
        self.updateCategoryListbox()


    def editCategory(self):
        print("editCategory")


    def deleteCategory(self):
        try:
            product = my_gui.productSelection.returnValue()
        except:
            messageBox('Geen categorie geselecteerd', 'U heeft geen categorie geselecteerd. Selecteer een categorie voordat u deze verwijdert.', 'error')
            return
        print(product)


    def addCategory(self):
        print("addCategory")


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
        for bestaandProduct in self.transaction:
            if product == bestaandProduct[0]:
                bestaandProduct[1] += amount
                self.updateTransactionListbox()
                return
        self.transaction.append([product,amount, pricePerItem])
        self.updateTransactionListbox()


    def updateCategoryListbox(self):
        for category in self.categories:
            print(category)
            self.overview.insert('end', '{:<50}{:<7}'.format(category[0], category[1]))



if __name__ == "__main__":
    root = tkinter.Tk()
    my_gui = categoriesOverview(root)
    root.mainloop()