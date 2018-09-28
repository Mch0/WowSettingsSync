#!C:\Users\arnaud\AppData\Local\Programs\Python\Python37-32\python.exe

# On importe Tkinter
from datetime import date
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
import os
import shutil
import json
import requests

folder_path = ""
errors = ""
WOW_ACCOUNT_PATH = "/WTF/ACCOUNT"
WOW_WTF_PATH = "/WTF/"
TEXT_BROWSE_DEFAULT = "Racine WoW folder"
FILE_FORMAT = ".zip"
TOKEN_GDRIVE = "ya29.GlsmBkwyY-PJcQj_bvhzgk7w_izj6Ao7-UUVWsyQ0GgFdvZu9kQrXsdF2m_llg2TWyRXy7_HvVf3XNUUw2MDONp3K7fBd7hakpQ7qp9RyT90Fs5U7jsUO3iZjqLM"
CONST_PUSH = 1
CONST_PULL = 2

def getFileZipName():
    return "Account-" + getDateToday()

def testGDriveConnection():
    pushFileToGDrive("test.txt", "text/plain","test.txt")

def pushFileToGDrive(filepath, filetype, filename):
    folderId = "1SuCsIuaN9FA65kvV6lM5_FuXU9swNTxd"
    headers = {
        "Authorization": "Bearer " + TOKEN_GDRIVE}  # put ur access token after the word 'Bearer '
    para = {
        "name": filename,  # file name to be uploaded
        "parents": [folderId]
    # make a folder on drive in which you want to upload files; then open that folder; the last thing in present url will be folder id
    }
    files = {
        'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
        'file': (filetype, open(filepath, "rb"))
    # replace 'application/zip' by 'image/png' for png images; similarly 'image/jpeg' (also replace your file name)
    }
    success.set("Sending Zip file on GDrive")
    r = requests.post(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        headers=headers,
        files=files
    )
    if r.status_code != 200:
        errors.set("Error during uploading file ==> HTTPS CODE : " + str(r.status_code))
    else:
        success.set("Sending ok")

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
def getDateToday():
    return date.today().strftime('%d-%m-%Y')

def _sync():
    _clearMessagesBags()
    if _checkWowPath() != False:
        #make zip file of folder Account
        localVarFolderWow = folder_Wow + "/WTF/Account/"
        zipFilePath = shutil.make_archive(getFileZipName(), 'zip', localVarFolderWow)
        if(zipFilePath != None and zipFilePath != False and zipFilePath != ""):
            success.set("Zip file has been create in : " + folder_Wow + WOW_WTF_PATH + getFileZipName() + FILE_FORMAT)
            zipfile = folder_Wow + WOW_WTF_PATH + getFileZipName() + FILE_FORMAT
            os.rename(zipFilePath, folder_Wow + WOW_WTF_PATH + getFileZipName() + FILE_FORMAT)
            pushFileToGDrive(folder_Wow + WOW_WTF_PATH + getFileZipName() + FILE_FORMAT, "application/zip", getFileZipName())
        else:
            errors.set("Error : impossible to create zip archive")


# On crée une fenêtre, racine de notre interface
fenetre = Tk()

content = ttk.Frame(fenetre)
content.grid(column=0, row=0)
fenetre.title("Wow Sync Settings Account")

folder_path = StringVar()
errors = StringVar()
success = StringVar()
token = StringVar()
pushOrPull = IntVar()

##SET DEFAULT VAR
folder_path.set("Racine WoW folder")
token.set(TOKEN_GDRIVE)

## FOLDER PATH FIELD
folder_path1 = Entry(master=fenetre, textvariable=folder_path, width=100)
folder_path1.grid(row=2, column=0, sticky=E, pady=5, padx=5)

##BUTTON BROWSE FOLDER
button2 = Button(text="Browse", command=browse_button)
button2.grid(row=2, column=0, sticky=W, pady=5, padx=5)

## LABEL FOR TOKEN GDRIVE
label_tokenGDrive = Label(text="TOKEN GDRIVE :")
label_tokenGDrive.grid(row=3, column=0, sticky=W, pady=5, padx=5)

## TOKEN GDRIVE FIELD
tokenGDrive = Entry(master=fenetre, textvariable=token, width=100)
tokenGDrive.grid(row=3, column=0, sticky=E, pady=5, padx=5)

## LABEL FOR PUSH OR PULL
label_pushOrPull = Label(text="PUSH OR PULL SETTING ? :")
label_pushOrPull.grid(row=4, column=0, sticky=W, pady=5, padx=5)

## PUSH OR PULL RADIO
radio_push = Radiobutton(fenetre, text="Push", variable=pushOrPull, value=CONST_PUSH).grid(row=5, column=0, sticky=W, pady=5, padx=5)
radio_pull = Radiobutton(fenetre, text="Pull", variable=pushOrPull, value=CONST_PULL).grid(row=6, column=0, sticky=W, pady=5, padx=5)

##EMPTY LABEL LINE
label_empty_line = Label(height=2)
label_empty_line.grid(row=7)

##ERROR LABEL##
label_error_message = Label(height=2, textvariable=errors, fg="red")
label_error_message.grid(row=8)
##SUCESS LABEL##
label_success_message = Label(height=2, textvariable=success, fg="green")
label_success_message.grid(row=9)

##BUTTON EXIT
bouton_quitter = Button(fenetre, text="Quitter", command=fenetre.quit)
bouton_quitter.grid(row=10, column=1, sticky=E, pady=5, padx=5)

##BUTTON SYNC
bouton_sync = Button(fenetre, text="Synchroniser", command=_sync)
bouton_sync.grid(row=10, rowspan=3, column=0, sticky=W, pady=5, padx=5)

##BUTTON TEST CONNECTION
bouton_sync = Button(fenetre, text="Test GDrive connection", command=testGDriveConnection)
bouton_sync.grid(row=10, rowspan=3, column=0, sticky=E, pady=5, padx=5)

fenetre.rowconfigure(0, weight=1)
content.rowconfigure(5, weight=10)

cadre = Frame(fenetre, width=768, borderwidth=1)
cadre.grid(pady=5, padx=5)

fenetre.mainloop()