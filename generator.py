import pyotp
import time
import tkinter as tk
from tkinter import * 
from tkinter.ttk import *
import csv

# names = [] 
# keys = []

def returnCurrentPassword(selectedKey):
    var.set(pyotp.TOTP(selectedKey).now())
    print("returnCurrentPassword called: ", pyotp.TOTP(selectedKey).now(), selectedKey)
 
root = Tk()
root.geometry("750x375")

# frame = Frame(root)
# frame.pack()
var = StringVar()


label = Label(root, textvariable = var )
button = Button(root, text = "Update one time password", command = returnCurrentPassword("base32secret3232"))
button.pack()
label.pack()
root.mainloop()