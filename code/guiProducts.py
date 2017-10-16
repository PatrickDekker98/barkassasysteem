from tkinter import *
import sqlite3,time

def fetchProducts():
    db = sqlite3.connect('..\\barkassasysteem.db')
    cur = db.cursor()
    epochTime = int(str(time.time()).split('.')[0] + str(time.time()).split('.')[1][:3])
    cur.execute('''SELECT productId, name FROM product WHERE datetimeStart < ? AND (datetimeEnd > ? OR datetimeEnd IS NULL)''', (epochTime, epochTime))
    products = cur.fetchall()
    db.close()
    return products

def done():
    global choice
    choice = 'End'
    root.quit()

def returnProduct(productId):
    global choice
    choice = productId
    root.quit()

def call():
    global root, frameContent, choice
    root = Tk()
    total = ''
    frameTitle = Frame(root)
    frameMenu = Frame(root)
    frameContent = Frame(root)
    frameTitle.pack(side='top',fill='x')
    frameMenu.pack(side='top',fill='x')
    frameContent.pack(side='top', fill='x')

    r = 0
    c = 0
    for product in fetchProducts():
        cmd = lambda id=product[0]: returnProduct(id)
        Button(frameContent, text=product[1], font=('Arial', 15), height=10, width=20, command=cmd).grid(row=r,column=c)
        c += 1
        if c > 2:
            c = 0
            r += 1
    Button(frameContent, text='Afrekenen', font=('Arial', 15), height=10, width=20, bg='light green', command=done).grid(row=3, column=2)
    root.mainloop()
    root.destroy()
    return choice