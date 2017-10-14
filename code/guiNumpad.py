from tkinter import *

def addOne():
    global total
    total = total + '1'
    labelTotaal.config(text=total)

def addTwo():
    global total
    total = total + '2'
    labelTotaal.config(text=total)

def addThree():
    global total
    total = total + '3'
    labelTotaal.config(text=total)

def addFour():
   global total
   total = total + '4'
   labelTotaal.config(text=total)

def addFive():
    global total
    total = total + '5'
    labelTotaal.config(text=total)

def addSix():
    global total
    total = total + '6'
    labelTotaal.config(text=total)

def addSeven():
    global total
    total = total + '7'
    labelTotaal.config(text=total)

def addEight():
    global total
    total = total + '8'
    labelTotaal.config(text=total)

def addNine():
    global total
    total = total + '9'
    labelTotaal.config(text=total)

def addZero():
    global total
    total = total + '0'
    labelTotaal.config(text=total)

def backspace():
    global total
    total = total[:-1]
    labelTotaal.config(text=total)

def done():
    global total,root
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
    Button(frameNumpad, text="9", font=('Arial', 20), command=addNine, height=5, width=10).grid(row=1, column=2)
    Button(frameNumpad, text="8", font=('Arial', 20), command=addEight, height=5, width=10).grid(row=1, column=1)
    Button(frameNumpad, text="7", font=('Arial', 20), command=addSeven, height=5, width=10).grid(row=1, column=0)
    Button(frameNumpad, text="6", font=('Arial', 20), command=addSix, height=5, width=10).grid(row=2, column=2)
    Button(frameNumpad, text="5", font=('Arial', 20), command=addFive, height=5, width=10).grid(row=2, column=1)
    Button(frameNumpad, text="4", font=('Arial', 20), command=addFour, height=5, width=10).grid(row=2, column=0)
    Button(frameNumpad, text="3", font=('Arial', 20), command=addThree, height=5, width=10).grid(row=3, column=2)
    Button(frameNumpad, text="2", font=('Arial', 20), command=addTwo, height=5, width=10).grid(row=3, column=1)
    Button(frameNumpad, text="1", font=('Arial', 20), command=addOne, height=5, width=10).grid(row=3, column=0)
    Button(frameNumpad, text="<", font=('Arial', 20), command=backspace, bg='red', height=5, width=10).grid(row=4,column=0)
    Button(frameNumpad, text="0", font=('Arial', 20), command=addZero, height=5, width=10).grid(row=4, column=1)
    Button(frameNumpad, text="Klaar", font=('Arial', 20), command=done, bg='lightgreen', height=5, width=10).grid(row=4, column=2)
    root.mainloop()
    root.destroy()
    return total
