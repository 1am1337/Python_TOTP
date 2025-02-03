import pyotp
import time
import tkinter as tk
from tkinter import * 
from tkinter.ttk import *
import csv

names = [] 
keys = []

def returnCurrentPassword(selectedKey):
    currentPassword.set(pyotp.TOTP(selectedKey).now())
    #print("returnCurrentPassword called: ", pyotp.TOTP(selectedKey).now(), selectedKey)
def openFile():
    with open('usr_data.csv', newline = '') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            names.append(row["names"]) 
            keys.append(row["keys"])   
def closeFile():  
    with open('usr_data.csv', 'w', newline='') as csvfile:      
        fieldnames = ['names', 'keys']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(len(names)):
            writer.writerow({'names': names[i], 'keys': keys[i]})  
def click_bind(e):
    indexKeyNames = names.index(keyNameSelection.get())
    selectedKey.set(keys[indexKeyNames])
    #print(indexKeyNames, selectedKey.get()) 
    returnCurrentPassword(selectedKey.get())

openFile()
root = Tk()
root.geometry("750x375")

currentPassword = StringVar()
currentPassword.set("press button??")
selectedKey = StringVar()
countryvar = StringVar()

keyNameSelection = Combobox(root, values = names)
keyNameSelection.state(["readonly"])
keyNameSelection.bind('<<ComboboxSelected>>',click_bind)


label = Label(root, textvariable = currentPassword)
button = Button(root, text = "Update one time password", command = lambda:returnCurrentPassword(selectedKey.get()))
button.pack()
label.pack()
keyNameSelection.pack()

# print(names, keys)
root.mainloop()
closeFile()