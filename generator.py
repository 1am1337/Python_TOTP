import pyotp
import time
import dearpygui.dearpygui as dpg
import csv

names = [] 
keys  = []
with open('usr_data.csv', newline = '') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        names.append(row["names"]) 
        keys.append(row["keys"])
dpg.create_context()
dpg.create_viewport(title = 'TOTP Generator', width = 400, height = 200)

def MatchIndex(sender):
    dpg.set_value("SelectedKey", keys[names.index(dpg.get_value(sender))])
    totp = pyotp.TOTP(keys[names.index(dpg.get_value(sender))])
    dpg.set_value("GeneratedPassword", totp.now()) 
    dpg.set_value("SelectedKey", keys[names.index(dpg.get_value(sender))])

with dpg.value_registry():
    dpg.add_string_value(default_value = "Select a Key!", tag = "SelectedKey")
    dpg.add_string_value(default_value = "Select a Key!", tag = "GeneratedPassword")
    
with dpg.window(label = "TOTP Generator", tag = "PrimaryWindow"): 
    with dpg.menu_bar():
        with dpg.menu(label = "Generate Passwords"):
            dpg.add_combo(items = (names), callback = MatchIndex)
            dpg.add_text(label = "Selected TOTP Key", source = "SelectedKey")
            dpg.add_input_text(label = "Current TOTP", source = "GeneratedPassword")
        with dpg.menu(label = "Configure Keys", indent = (-300)):
            dpg.add_input_text(default_value = "Enter a Name", label = "Name", on_enter = True)
            dpg.add_input_text(default_value = "Enter your TOTP Key", label = "TOTP Key (base32)", on_enter = True)
            with open('usr_data.csv', 'w', newline='') as csvfile:
                fieldnames = ['names', 'keys']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for i in range(len(names)):
                    writer.writerow({'names': names[i], 'keys': keys[i]})
            with open('usr_data.csv', newline = '') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    names.append(row["names"]) 
                    keys.append(row["keys"])
            with dpg.collapsing_header(label = "Show All Keys/Names"):
                with dpg.table(header_row=True):
                    dpg.add_table_column(label="Names")
                    dpg.add_table_column(label="Keys")
                    for i in range(len(names)):
                        with dpg.table_row():
                            for j in range(len(names)):
                                if i >= 0 and j == 0:
                                    dpg.add_text(names[i])
                                elif j == 1:
                                    dpg.add_text(keys[i])


dpg.setup_dearpygui()
dpg.set_primary_window("PrimaryWindow", True)
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()