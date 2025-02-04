# totp updates at xx:xx:00 and xx:xx:30 -> implement timer

import pyotp
import time
import tkinter as tk
from tkinter import * 
from tkinter.ttk import *
import csv

names = [] 
keys = []
standardTextValue = "Select a Key first :)"
widthVal = 800

def updateOTP(selectedKey):
    if currentPassword.get() == standardTextValue or currentPassword.get() == "nothing to copy!":
        currentPassword.set(standardTextValue)
    else:
        currentPassword.set(pyotp.TOTP(selectedKey).now())
    

def openFile():
    with open('usr_data.csv', newline = '') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            names.append(row["names"]) 
            keys.append(row["keys"])   


def writeFile(): 
    with open('usr_data.csv', 'w', newline='') as csvfile:      
        fieldnames = ['names', 'keys']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(len(names)):
            writer.writerow({'names': names[i], 'keys': keys[i]}) 


def click_bind(e):
    selectedKey.set(keys[names.index(keyNameSelection.get())])
    currentPassword.set(pyotp.TOTP(selectedKey.get()).now())
    updateCombobox()



def copyKey():
    if currentPassword.get() == standardTextValue or currentPassword.get() == "nothing to copy!":
        currentPassword.set("nothing to copy!")
    else:
        root.clipboard_clear()
        root.clipboard_append(currentPassword.get())


def setNewNameKeyPair():
    names.append(NameInput.get())
    keys.append(KeyInput.get())
    NameKeyTable.insert("", tk.END, text=NameInput.get(), values=KeyInput.get())
    updateCombobox()
    writeFile()


def SetGrid():
    tabControl.grid(column=0,row=0)
    label.grid(column=0, row=1)
    updateButton.grid(column=1, row=1)
    keyNameSelection.grid(column=0, row=2)
    copyButton.grid(column=1, row=2)
    NameKeyTable.grid(column = 0, row = 3)
    NameInput.grid(column = 0, row = 4, sticky ="w")
    NameInputLabel.grid(column = 0, row = 4,sticky="e")
    KeyInput.grid(column = 0, row = 5, sticky="w")
    KeyInputLabel.grid(column = 0, row = 5, sticky="e")
    commitChangesButton.grid(column = 0, row = 6)


def updateCombobox():
    keyNameSelection.configure(values=names)

    
openFile()
root = Tk()
root.geometry(f"{widthVal}x400")
root.minsize(widthVal, 400)
root.maxsize(widthVal, 400)
tabControl = Notebook(root)


GenTab = Frame(tabControl)
SetTab = Frame(tabControl)

tabControl.add(GenTab, text="Generation")
tabControl.add(SetTab, text="Add new Key")

selectedKey = StringVar()
currentPassword = StringVar()
currentPassword.set(standardTextValue)

keyNameSelection = Combobox(GenTab, state = "readonly", values = names)
keyNameSelection.bind('<<ComboboxSelected>>', click_bind)
copyButton = Button(GenTab, text = "copyButton", command = copyKey)
label = Label(GenTab, textvariable = currentPassword)
updateButton = Button(GenTab, text = "UpdateOTP", command = lambda: updateOTP(selectedKey.get()))


NameKeyTable = Treeview(SetTab, columns=('Keys'))
NameKeyTable.heading("#0", text = "Names")
NameKeyTable.column("#0", minwidth=0, width=100, stretch=NO)
NameKeyTable.heading("Keys", text = "Keys")
NameKeyTable.column("Keys", minwidth=0, width=round(widthVal*0.8), stretch=NO)
for i in range(len(names)):
    NameKeyTable.insert(
        "",
        tk.END,
        text= names[i],
        values=keys[i]
    )

NameInput = Entry(SetTab, width=(round(widthVal*0.08)))
NameInputLabel = Label(SetTab, text= "NameInput")
KeyInput = Entry(SetTab,  width=(round(widthVal*0.08)))
KeyInputLabel = Label(SetTab, text= "KeyInput")
commitChangesButton = Button(SetTab, text="commitChanges", command = setNewNameKeyPair)


SetGrid()
root.mainloop()

