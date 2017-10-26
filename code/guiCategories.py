from main import *
import categories


class categoriesOverview(tkinter.Frame):
    categories = []
    total = 0

    def __init__(self, master):
        self.master = master
        self.overview = tkinter.Listbox(self.master, width=55)
        self.overview.grid(column=0, row=1, columnspan=4)
        tkinter.Label(self.master, text="{:20}     {:3}".format('ID', 'Naam'), font=('Arial', 10)).grid(column=0, row=0,columnspan=2, sticky='w')
        tkinter.Button(self.master, text="Aanpassen", font=('Arial', 20), height=1, width=10, bg='#5AF', command=self.editCategory).grid(column=0, row=3)
        tkinter.Button(self.master, text="Verwijderen", font=('Arial', 20), height=1, width=10, bg='#F88',command=self.deleteCategory).grid(column=1, row=3)
        tkinter.Button(self.master, text="Nieuwe categorie", font=('Arial', 20), height=1, width=20, bg='#8F8',command=self.addCategory).grid(column=0, row=4,columnspan=2)
        self.setCategories()
        self.updateCategoryListbox()


    def setCategories(self):
        data = categories.getCategories()
        self.categories = []
        for row in data:
            self.categories.append(row)

    def editCategory(self):
        category = self.categories[self.overview.index('active')]
        input = simpledialog.askstring("Categorie", "Pas deze categorie aan", initialvalue=category[1])
        if categories.updateCategory(category[0], input):
            self.setCategories()
            self.updateCategoryListbox()


    def deleteCategory(self):
        try:
            category = categories[self.overview.index('active')]
            if categories.deleteCategory(category[0]):
                self.setCategories()
                self.updateCategoryListbox()
        except:
            messageBox('Geen categorie geselecteerd', 'U heeft geen categorie geselecteerd. Selecteer een categorie voordat u deze verwijdert.', 'error')
            return


    def addCategory(self):
        input = simpledialog.askstring("Categorie", "Voeg een categorie toe")
        if categories.addCategory(input):
            self.setCategories()
            self.updateCategoryListbox()



    def updateCategoryListbox(self):
        self.overview.delete(0, "end")
        for category in self.categories:
            self.overview.insert('end', '{:<50}{:<7}'.format(category[0], category[1]))
