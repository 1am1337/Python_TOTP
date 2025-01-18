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
amountNames = len(names)                                                                #bishierhin alles initierprozess

dpg.create_context()
dpg.create_viewport(title = 'TOTP Generator', width = 400, height = 300)                #erstellt das fenster


def _logKey(sender, app_data, user_data):                                               #fügt den oben erstellten listen neue daten hinzu
    global names                                                                        #soll man eig nicht; dachte funktioniert; macht aber nicht :(                 
    if sender == "newName":
        names.append(app_data)
        amountNames = len(names)
        names = names
    elif sender == "newKey":
        keys.append(app_data)
        amountNames = len(names)
        names = names

def MatchIndex(sender):                                                                 #gibt als output das totp passwort aus und sagt welcher generiert wurde
    dpg.set_value("SelectedKey", keys[names.index(dpg.get_value(sender))])
    totp = pyotp.TOTP(keys[names.index(dpg.get_value(sender))])
    dpg.set_value("GeneratedPassword", totp.now()) 

with dpg.value_registry():
    dpg.add_string_value(default_value = "Select a Key!", tag = "SelectedKey")          #setzt start informationen
    dpg.add_string_value(default_value = "Select a Key!", tag = "GeneratedPassword")
    
with dpg.window(label = "TOTP Generator", tag = "PrimaryWindow"): 
    with dpg.menu_bar():                                                                                                    #erstellt eine menü leiste
        with dpg.menu(label = "Generate Passwords"):                                                                        #erstellt das menü für passwort generation
            dpg.add_combo(items = (names), callback = MatchIndex)                                                           #dropdown menü mit (theoretisch) allen gespeicherten werten
            dpg.add_text(label = "Selected TOTP Key", source = "SelectedKey")                                               #textfeld
            dpg.add_input_text(label = "Current TOTP\t\t\t", source = "GeneratedPassword")                                  #muss input_text sein, sonst kann man nichts markieren

        with dpg.menu(label = "Configure Keys"):                                                                            #erstellt das memü für name/key speicherung
            dpg.add_input_text(label = "Name", on_enter = True, tag = "newName", callback = _logKey)                        #erstellungs feld für name v. key
            dpg.add_input_text(label = "TOTP Key (base32)\t\t", on_enter = True, tag = "newKey", callback = _logKey)        #erstellungs feld für key 
            with dpg.collapsing_header(label = "Show All Keys/Names"):                                                      #zeigt tabelle mit (theoretisch) allen gespeicherten namen/key paaren
                with dpg.table(header_row=True):
                    dpg.add_table_column(label="Names")
                    dpg.add_table_column(label="Keys")
                    for i in range(amountNames):
                        with dpg.table_row():
                            for j in range(amountNames):
                                if i >= 0 and j == 0:
                                    dpg.add_text(names[i])
                                elif j == 1:
                                    dpg.add_text(keys[i])
                                                                                                                            #wahrscheinliche fehlerquelle: es wird bei listen immer nur einmal gecheckt, was drin ist/wie lang die liste ist

dpg.setup_dearpygui()
dpg.set_primary_window("PrimaryWindow", True)                   #setzt das fenster im fenster auf "vollbildschirm"
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
with open('usr_data.csv', 'w', newline='') as csvfile:          #schreibt die beiden listen wieder in die csv datei; speichert quasi alles
    fieldnames = ['names', 'keys']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(len(names)):
        writer.writerow({'names': names[i], 'keys': keys[i]})

