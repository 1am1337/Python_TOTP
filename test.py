import tkinter as tk
from tkinter import * 
from tkinter.ttk import *



root = Tk()

root.title("TTK Bootstrap! Combobox")
root.geometry('500x350')

# Create button click function
def clicker():
    my_label.config(text=f"You Clicked On {my_combo.get()}!")

# Create Binding function
def click_bind(e):
    my_label.config(text=f"You Clicked On {my_combo.get()}!")

# Create Label
my_label = Label(root, text="Hello World!", font=("Helvetica", 18))
my_label.pack(pady=30)

# Create Dropdown options
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Create Combobox
my_combo = Combobox(root, values=days)
my_combo.pack(pady=20)

# Set Combo Default
my_combo.current(0)

# Create a button
my_button = Button(root, text="Click Me!", command=clicker)
my_button.pack(pady=20)

# Bind the combobox
my_combo.bind('<<ComboboxSelected>>', click_bind)


root.mainloop()