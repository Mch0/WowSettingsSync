#!C:\Users\arnaud\AppData\Local\Programs\Python\Python37-32\python.exe
# On importe Tkinter
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
import os
import zipfile
import shutil
folder_path = ""
errors = ""
WOW_ACCOUNT_PATH = "/WTF/ACCOUNT"
WOW_WTF_PATH = "/WTF/"
TEXT_BROWSE_DEFAULT = "Racine WoW folder"

def _clearMessagesBags():
    success.set("")
    errors.set("")

def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
def _checkWowPath():
    if (folder_path.get() != "" and folder_path.get() != None and folder_path.get() != TEXT_BROWSE_DEFAULT):
        global folder_Wow
        folder_Wow = folder_path.get()
        return True
    else:
        errors.set("No folder path defined for Wow Path !")
        return False

def _sync():
    _clearMessagesBags()
    if _checkWowPath() != False:
        #make zip file of folder Account
        localVarFolderWow = folder_Wow + "/WTF/Account/"
        zipFilePath = shutil.make_archive("Account", 'zip', localVarFolderWow)
        if(zipFilePath != None and zipFilePath != False and zipFilePath != ""):
            success.set("Zip file has been create in : " + folder_Wow + WOW_WTF_PATH + "Account.zip")
        os.rename(zipFilePath, folder_Wow + WOW_WTF_PATH + "Account.zip")


# On crée une fenêtre, racine de notre interface
fenetre = Tk()

content = ttk.Frame(fenetre)
content.grid(column=0, row=0)
fenetre.title("Wow Sync Settings Account")

folder_path = StringVar()
errors = StringVar()
success = StringVar()
folder_path.set("Racine WoW folder")
folder_path1 = Entry(master=fenetre, textvariable=folder_path, width=100)
folder_path1.grid(row=2, column=0, sticky=E, pady=5, padx=5)

label_empty_line = Label(height=2)
label_empty_line.grid(row=3)

label_error_message = Label(height=2, textvariable=errors, fg="red")
label_error_message.grid(row=4)

label_success_message = Label(height=2, textvariable=success, fg="green")
label_success_message.grid(row=5)

button2 = Button(text="Browse", command=browse_button)
button2.grid(row=2, column=0, sticky=W, pady=5, padx=5)

bouton_quitter = Button(fenetre, text="Quitter", command=fenetre.quit)
bouton_quitter.grid(row=6, column=1, sticky=E, pady=5, padx=5)

bouton_sync = Button(fenetre, text="Synchroniser", command=_sync)
bouton_sync.grid(row=6, rowspan=3, column=0, sticky=W, pady=5, padx=5)

fenetre.rowconfigure(0, weight=1)
content.rowconfigure(5, weight=10)

cadre = Frame(fenetre, width=768, borderwidth=1)
cadre.grid(pady=5, padx=5)

fenetre.mainloop()