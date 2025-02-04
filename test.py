import tkinter as tk
from tkinter import * 
from tkinter.ttk import *



root = Tk()
tree = Treeview(root)
# Inserted at the root, program chooses id:
tree.insert('', 'end', 'widgets', text='Widget Tour')
 
# Same thing, but inserted as first child:
tree.insert('', 0, 'gallery', text='Applications')

# Treeview chooses the id:
id = tree.insert('', 'end', text='Tutorial')

# Inserted underneath an existing node:
tree.insert('widgets', 'end', text='Canvas')
tree.insert(id, 'end', text='Tree')

tree.grid()
root.mainloop()
