import time
import pyotp 
import dearpygui.dearpygui as dpg
import csv
names = [] 
keys  = []

with open('usr_data.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
    	names.append(row["name"]) 
    	keys.append(row["key"])

dpg.create_context()

def button_callback(sender, app_data):
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")

with dpg.window(label="Tutorial"):
    dpg.add_button(label="Print to Terminal", callback=button_callback)

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
# below replaces, start_dearpygui()
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()

dpg.destroy_context()