import pyotp
import time
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
dpg.create_viewport(title='TOTP Genrator', width=400, height=300)

# def GenerateCurrentToken():
#     print(sel, "GenerateCurrentToken")
#     totp = pyotp.TOTP(keys[sel])
#     dpg.set_value("GeneratedPassword", totp.now())

def MatchIndex(sender):
    dpg.set_value("SelectedKey", keys[names.index(dpg.get_value(sender))])
    totp = pyotp.TOTP(keys[names.index(dpg.get_value(sender))])
    dpg.set_value("GeneratedPassword", totp.now())


with dpg.value_registry():
    dpg.add_string_value(default_value="Click Generate!", tag="GeneratedPassword")
    dpg.add_string_value(default_value="Select a Key!", tag="SelectedKey")


with dpg.window(label="TOTP_FFXIV", tag="PrimaryWindow"):   
    button1 = dpg.add_button(label="Generate", callback = MatchIndex)
    dpg.add_combo(items=(names), callback=MatchIndex)
    dpg.add_input_text(label="Selected TOTP Key", source="SelectedKey")
    dpg.add_input_text(label="Current TOTP", source="GeneratedPassword")
    


dpg.setup_dearpygui()
dpg.set_primary_window("PrimaryWindow", True)
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()