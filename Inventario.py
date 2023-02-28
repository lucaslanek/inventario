import os
import schedule
import gspread
import Requests as rq
import threading
from time import sleep
from datetime import datetime, time
from oauth2client.service_account import ServiceAccountCredentials

Entry_key = '17H_Z_kJcqJBX4A0LKizI4A450V_y0nI3Qu4tq9UP4n8'
Stock_key = '1Qqxaof92dIeP--Vy3B62l3pEnL_FG42SdzEV9Kxy0fI'
Outs_key  = '1sZK9-F7PN4xCzU2q2fMNbR7U1CGnMUbAlUhAKVAJJ2c'

#sheet_key = '1G8SWQ-Z9TiFGGIV-oAnlJCKjkNLWtPVjXRkLSbNnixE'

gc = gspread.service_account(filename='credentials.json')
Entry_sheet = gc.open_by_key(Entry_key)
Outs_sheet = gc.open_by_key(Outs_key)
Stock_sheet = gc.open_by_key(Stock_key)

Ent_sheet = Entry_sheet.worksheet('Entradas')
Out_sheet = Outs_sheet.worksheet('Salidas')
Inv_sheet = Stock_sheet.worksheet('Inventario')


last_edited_entry   = datetime.strptime(Ent_sheet.col_values(2)[-1], '%d/%m/%Y %H:%M:%S').time()
last_edited_out     = datetime.strptime(Out_sheet.col_values(1)[-1], '%d/%m/%Y %H:%M:%S').time()

if not os.path.exists("log.txt"):
    with open("log.txt", "w") as file:
        pass

if not os.path.exists("entries.txt"):
    with open("entries.txt", "w") as file:
        pass

if not os.path.exists("outs.txt"):
    with open("outs.txt", "w") as file:
        pass

def inventario():
    try:
        #total_rows = len(Ent_sheet.col_values(2)) - 1   #only data

        edited_entry    = datetime.strptime(Ent_sheet.col_values(2)[-1], '%d/%m/%Y %H:%M:%S').time()
        edited_out      = datetime.strptime(Out_sheet.col_values(1)[-1], '%d/%m/%Y %H:%M:%S').time()

        if edited_entry > last_edited_entry : 
            Entry_t = threading.Thread(target=rq.New_entry, args=(Ent_sheet, Inv_sheet))
            #rq.New_entry(Ent_sheet, Inv_sheet)
            Entry_t.start()
            last_edited_entry = edited_entry
            print("Entry updated at "+str(last_edited_entry))

            with open("log.txt", "a") as file:
                file.write("Entry updated at "+str(last_edited_entry) + "\n")

        elif edited_out > last_edited_out : 
            Out_t = threading.Thread(target=rq.New_out, args=(Out_sheet, Inv_sheet))
            #rq.New_out(Out_sheet, Inv_sheet)
            Out_t.start()
            last_edited_out = edited_out
            print("Out updated at "+str(last_edited_out))

            with open("log.txt", "a") as file:
                file.write("Out updated at "+str(last_edited_entry) + "\n")
            
        print("Waiting")

    except Exception as e:
        # Print the error message
        print("An error occurred:", str(e))
        with open("log.txt", "a") as file:
            file.write("Error : \n" + str(e) + "\n")

def main():
    schedule.every(10).seconds.do(inventario)


if __name__ == "__main__":
    main()