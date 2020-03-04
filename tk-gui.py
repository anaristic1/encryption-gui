import tkinter as tk
from tkinter import Text
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkinter.filedialog import askopenfilename
from cryptography import encrypt_aes,encrypt_salsa20,encrypt_3des,decrypt_aes,decrypt_salsa20,decrypt_3des
from Crypto.Random import get_random_bytes
from database import get_specific_rows
from base64 import b64decode
file_path = ""


def get_type():
    return file_path.split(".")[1]


def get_name():
    return file_path.split("/")[-1].split(".")[0]


def write_in_txt(text, path):
    with open(path, "w") as f:
        f.write(text)


def choose_file():
    global file_path

    file_path = askopenfilename(filetypes=[("Txt", "*.txt"), ("JPG", "*.jpg"), ("ENC", "*.enc"),("PDF", "*.pdf")])

    messagebox.showinfo("Error", "No file chosen!") if file_path == "" else message.configure(
        text=f"Chosen file: {get_name()}" if len(get_name()) < 30 else f"{get_type()} file chosen")


def write_text():
    """Creates a new window in which text can be written and saved."""
    def retrieve_input():
        global file_path
        input_text = txt.get("1.0", 'end-1c')
        if input_text == "":
            ok_message.configure(fg="red", text="No text!")
        elif len(input_text) > 50:
            ok_message.configure(fg="red", text="To much text!")
        else:
            file_path = "C:/Users/Ana/Desktop/message.txt"
            write_in_txt(input_text, file_path)
            message.configure(text="Text saved")
            new_window.destroy()

    new_window = tk.Toplevel(window)
    new_window.grab_set()
    new_window.title("Write text")
    new_window.resizable(width=False, height=False)
    txt = Text(new_window, width=30, height=5)
    ok_btn = tk.Button(new_window, text="Ok", command=retrieve_input)
    ok_message = tk.Label(new_window)
    txt.grid(column=0, row=0)
    ok_btn.grid(column=0, row=1)
    ok_message.grid(column=0, row=2)


def modified(event):
    print(combo.get())


def check():
    global file_path
    if message != "":
        message.configure(text="")
    if file_path == "":
        messagebox.showinfo("No file", "No file chosen!")
        return False
    elif combo.get() not in values:
        messagebox.showinfo("No algorithm", "No algorithm chosen!")
        return False
    return True


def encrypt_file():
    global file_path

    if not check():
        return
    else:
        if get_type() == "enc":
            messagebox.showinfo("Wrong type", "Chosen file is .enc type!")
        else:
            algorithm = combo.get()
            if algorithm == 'AES':
                encrypt_aes(get_random_bytes(16), file_path)
            elif algorithm == 'Salsa20':
                encrypt_salsa20(get_random_bytes(32), file_path)
            elif algorithm == '3DES':
                encrypt_3des(file_path)


def decrypt_file():
    if not check():
        return
    else:
        try:
            row = get_specific_rows(file_path, combo.get())
            algorithm = row[0][1]
            key = row[0][4]
            iv = row[0][5]
            cipher_path = row[0][2]
            filetype = row[0][3]
            print(type(key), type(iv),type(file_path),type(filetype))
            if algorithm == 'AES':
                 decrypt_aes(key,iv,cipher_path,filetype)
            elif algorithm == 'Salsa20':
                decrypt_salsa20(key,iv,cipher_path,filetype)
            elif algorithm == '3DES':
                decrypt_3des(key,iv,cipher_path,filetype)

            decrypt_window = tk.Toplevel(window)
            decrypt_window.grab_set()
            decrypt_window.title("Decrypt")
            decrypt_window.resizable(width=False, height=False)
            lbl_row1 = tk.Label(decrypt_window,font=("Arial", 12), text="Key:")
            text1 = tk.Label(decrypt_window,text=row[0][4])
            lbl_row2 = tk.Label(decrypt_window, font=("Arial", 12), text="Iv:")
            text2 = tk.Label(decrypt_window,text=(row[0][5]))
            lbl_row1.grid(column=0, row=0)
            text1.grid(column=1, row=0)
            lbl_row2.grid(column=0, row=1)
            text2.grid(column=1, row=1)
            messagebox.showinfo("Success","File was decrypted")
        except Exception as e:
            print("Error"+e.message)


#  Main GUI elements
window = tk.Tk()
window.title("ZRS Projekat")
window.resizable(width=False,height=False)
window.geometry('500x400')

lbl1 = tk.Label(window, font=("Arial", 12), text="Choose from computer")
open_file_btn = tk.Button(window, text="Choose file", bg="black", fg="white", command=choose_file)
lbl2 = tk.Label(window, font=("Arial", 12), fg="red", text="OR")
lbl3 = tk.Label(window, font=("Arial", 12), text="Write text")
write_text_btn = tk.Button(window, text="Write", bg="black", fg="white", command=write_text)
message = tk.Label(window, font=("Arial", 12))

values = ["AES", "3DES", "Salsa20"]
combo = Combobox(window, values=values, state='readonly')
combo.bind('<<ComboboxSelected>>', modified)
lbl4 = tk.Label(window, font=("Arial", 12), text="Choose an algorithm:")
empty = tk.Label(window)  # used for better look in GUI

lbl5 = tk.Label(window, font=("Arial", 12), text="Choose encryption/decryption:")
encrypt_btn = tk.Button(window, text="Encrypt", bg="black", fg="white", command=encrypt_file)
decrypt_btn = tk.Button(window, text="Decrypt", bg="black", fg="white", command=decrypt_file)
message2 = tk.Label(window, font=("Arial", 12), text="")


#  Main GUI grid
lbl1.grid(column=0, row=0, padx=10)
lbl2.grid(column=1, row=0)
lbl3.grid(column=2, row=0)
open_file_btn.grid(column=0, row=1)
write_text_btn.grid(column=2,row=1)
message.grid(column=1, row=2)
lbl4.grid(column=1, row=3)
combo.grid(column=1, row=4)
empty.grid(column=1, row=5)
lbl5.grid(column=0, row=6)
encrypt_btn.grid(column=1, row=6, pady=10)
decrypt_btn.grid(column=2, row=6)
message2.grid(column=1, row=7)

window.mainloop()