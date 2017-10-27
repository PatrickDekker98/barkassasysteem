from main import *


class categoriesOverview(tkinter.Frame):
    'Class for creating a tkinter GUI screen for manipulating the categories in the database'
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
        'Creates a list of all active categories, and saves this in self.categories'
        data = categories.getCategories()
        self.categories = []
        for row in data:    # Every category gets appended to self.categories
            self.categories.append(row)


    def editCategory(self):
        'Prompts the user and edits the category\'s name'
        category = self.categories[self.overview.index('active')]
        input = simpledialog.askstring("Categorie", "Pas deze categorie aan", initialvalue=category[1])
        if categories.updateCategory(category[0], input):
            self.setCategories()
            self.updateCategoryListbox()


    def deleteCategory(self):
        'Takes the selected category from the listBox and marks it as inactive in the database'
        try:
            category = self.categories[self.overview.index('active')]
            if categories.deleteCategory(category[0]):
                self.setCategories()
                self.updateCategoryListbox()
        except:
            tkinter.messagebox.showwarning('Geen categorie geselecteerd', 'U heeft geen categorie geselecteerd. Selecteer een categorie voordat u deze verwijdert.')
            return


    def addCategory(self):
        'prompts the user for a new category name, then creates a new category with this name'
        input = simpledialog.askstring("Categorie", "Voeg een categorie toe")
        if categories.addCategory(input):
            self.setCategories()
            self.updateCategoryListbox()


    def updateCategoryListbox(self):
        'Updates the Listbox with, by removing all content, then appends the entire list from scratch'
        self.overview.delete(0, "end")
        for category in self.categories:
            self.overview.insert('end', '{:<50}{:<7}'.format(category[0], category[1]))
