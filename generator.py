import pyotp
import time
import dearpygui.dearpygui as dpg
import csv

names = [] 
keys  = []
amountNames = len(names)
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

def _logKey(sender, app_data):                                                                                                    
    if sender == "newName":
        names.append(app_data)
        amountNames = len(names)
    elif sender == "newKey":
        keys.append(app_data)
        amountNames = len(names)
    print("_logKey called", app_data)

def MatchIndex(sender):                                                            
    dpg.set_value("SelectedKey", keys[names.index(dpg.get_value(sender))])
    totp = pyotp.TOTP(keys[names.index(dpg.get_value(sender))])
    dpg.set_value("GeneratedPassword", totp.now())
    print("matchIndexCalled", names, keys)


def main():
    openFile()    
    dpg.create_context()            
    with dpg.window(label = "TOTP Generator", tag = "PrimaryWindow"): 
        with dpg.menu_bar():                                                                                                    
            with dpg.menu(label = "Generate Passwords"):                                                                        
                dpg.add_combo(items = (names), callback = MatchIndex)                                                           
                dpg.add_text(label = "Selected TOTP Key", tag = "SelectedKey", default_value = "Select a Key!")              
                dpg.add_input_text(label = "Current TOTP\t\t\t", tag = "GeneratedPassword", default_value = "Generate a Password")                                                                   
            with dpg.menu(label = "Configure Keys"):                                                                            
                dpg.add_input_text(label = "Name", on_enter = True, tag = "newName", callback = _logKey)                        
                dpg.add_input_text(label = "TOTP Key (base32)\t\t", on_enter = True, tag = "newKey", callback = _logKey)        
                with dpg.collapsing_header(label = "Show All Keys/Names"):  
                    print("collapsing_header called")                                                    
                    with dpg.table(header_row=True):
                        dpg.add_table_column(label="Names", tag = "Names")
                        dpg.add_table_column(label="Keys", tag = "keys")
                        for i in range(amountNames):
                            with dpg.table_row():
                                for j in range(amountNames):
                                    if i >= 0 and j == 0:
                                        dpg.add_text(names[i])
                                    elif j == 1:
                                        dpg.add_text(keys[i])
    dpg.create_viewport(title = 'TOTP Generator', width = 400, height = 300)
    dpg.setup_dearpygui()
    dpg.set_primary_window("PrimaryWindow", True)                  
    dpg.show_viewport()
    dpg.start_dearpygui()
    closeFile()
    dpg.destroy_context()

main()


