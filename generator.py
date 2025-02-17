import pyotp
import time
import tkinter as tk
from tkinter import * 
from tkinter.ttk import *
import csv
from datetime import datetime
from pathlib import Path

names = [] 
keys = []
standardTextValue = "Select a Key first :)"
widthVal = 800
fileLocation = Path("usr_data.csv")


def getCurrentSeconds():
    return 30 - (datetime.now().second % 30)


def updateTime():
    if getCurrentSeconds() == 1:
        remainingSeconds.set("OTP  is now invalid")
    else:
        remainingSeconds.set(f"OTP valid for {getCurrentSeconds()} seconds")
        root.after(1000, updateTime)
            


def updateOTP(selectedKey):
    if currentPassword.get() == standardTextValue or currentPassword.get() == "Nothing to copy!":
        currentPassword.set(standardTextValue)
    else:
        currentPassword.set(pyotp.TOTP(selectedKey).now())
        updateTime()


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
    if currentPassword.get() == standardTextValue or currentPassword.get() == "Nothing to copy!":
        currentPassword.set("Nothing to copy!")
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
    passwordLabel.grid(column=0, row=1)
    remainingTimeLabel.grid(column=2, row=1)
    updateButton.grid(column=1, row=1, sticky ="e")
    keyNameSelection.grid(column=0, row=2)
    copyButton.grid(column=1, row=2, sticky="e")
    NameKeyTable.grid(column = 0, row = 3)
    NameInput.grid(column = 0, row = 4, sticky ="w")
    NameInputLabel.grid(column = 0, row = 4,sticky="e")
    KeyInput.grid(column = 0, row = 5, sticky="w")
    KeyInputLabel.grid(column = 0, row = 5, sticky="e")
    commitChangesButton.grid(column = 0, row = 6, sticky="w")
    deleteButton.grid(column = 0, row = 6, sticky="e")

def deleteKeyNamePair():
    itemToDelete = NameKeyTable.focus()
    NameKeyTable.delete(itemToDelete)
    keys.remove(keys[names.index(itemToDelete)])
    names.remove(itemToDelete)
    updateCombobox()
    writeFile()

def updateCombobox():
    keyNameSelection.configure(values=names)



if fileLocation.is_file():
    openFile()
else:
    writeFile()



root = Tk()
root.geometry(f"{widthVal}x400")
root.minsize(widthVal, 400)
root.maxsize(widthVal, 400)
tabControl = Notebook(root)


GenTab = Frame(tabControl)
SetTab = Frame(tabControl)

tabControl.add(GenTab, text="Password Generation")
tabControl.add(SetTab, text="Add new Key")

selectedKey = StringVar()
currentPassword = StringVar()
currentPassword.set(standardTextValue)

remainingSeconds = StringVar()
remainingSeconds.set(" ")

keyNameSelection = Combobox(GenTab, state = "readonly", values = names)
keyNameSelection.bind('<<ComboboxSelected>>', click_bind)
copyButton = Button(GenTab, text = "Copy OTP", command = copyKey, width = 10)
passwordLabel = Label(GenTab, textvariable = currentPassword)
updateButton = Button(GenTab, text = "Update OTP", command = lambda: updateOTP(selectedKey.get()), width = 10)
remainingTimeLabel = Label(GenTab, textvariable = remainingSeconds)


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
        values=keys[i],
        iid = names[i]
    )

NameInput = Entry(SetTab, width=(round(widthVal*0.075)))
NameInputLabel = Label(SetTab, text= "Enter an arbitrary Name")
KeyInput = Entry(SetTab,  width=(round(widthVal*0.075)))
KeyInputLabel = Label(SetTab, text= "Input your TOTP Key here")
commitChangesButton = Button(SetTab, text="Add Key to list", command = setNewNameKeyPair)
deleteButton = Button(SetTab, text="Delete selected TOTP key", command = deleteKeyNamePair)


SetGrid()
root.mainloop()

