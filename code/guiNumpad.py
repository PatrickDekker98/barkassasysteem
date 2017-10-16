from tkinter import *

def add(number):
    global total
    total = total + str(number)
    labelTotaal.config(text=total)

def backspace():
    global total
    total = total[:-1]
    labelTotaal.config(text=total)

def done():
    global total
    if total != '':
        root.quit()
    else:
        labelTotaal.config(text='0')
    return total

def call(productnaam):
    global total,labelTotaal,root
    root = Tk()
    total = ''
    frameTitle = Frame(root)
    frameNumpad = Frame(root)
    frameTitle.pack(side='top',fill='x')
    frameNumpad.pack(side='top', fill='x')
    Label(frameTitle, text="Aantal {}:".format(productnaam), font=('Arial', 20), height=5).grid(row=0, column=0, columnspan=2)
    labelTotaal = Label(frameTitle, text='', font=('Arial', 25, 'bold'))
    labelTotaal.grid(row=2, column=2)
    buttons = ['7', '8', '9', '4', '5', '6', '1', '2', '3']
    r = 0
    c = 0
    for b in buttons:
        cmd = lambda button=b: add(button)
        Button(frameNumpad, text=b, font=('Arial', 20), height=5, width=10, command=cmd).grid(row=r, column=c)
        c += 1
        if c > 2:
            c = 0
            r += 1
    Button(frameNumpad, text='<', font=('Arial', 20), height=5, width=10, bg='red', command=backspace).grid(row=3, column=0)
    Button(frameNumpad, text='0', font=('Arial', 20), height=5, width=10, command=lambda: add(0)).grid(row=3,column=1)
    Button(frameNumpad, text='Klaar', font=('Arial', 20), height=5, width=10, bg='light green', command=done).grid(row=3, column=2)
    root.mainloop()
    root.destroy()
    return total