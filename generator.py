import time
import pyotp 
from nicegui import ui

ui.label('Hello NiceGUI!')

ui.run()

import csv
names = [] 
keys  = []

with open('usr_data.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
    	names.append(row["name"]) 
    	keys.append(row["key"])

