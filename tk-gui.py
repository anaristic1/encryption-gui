import tkinter as tk
from tkinter import Text
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkinter.filedialog import askopenfilename


file_path = ""

def get_type():
    return file_path.split(".")[1]


def get_name():
    return file_path.split("/")[-1].split(".")[0]


def write_in_txt(text, path):
    with open(path, "w") as f:
        f.write(text)


def choose_file():
    """Chooses file path and creates a class depending on the file type."""
    global file_path

    try:
        file_path = askopenfilename(filetypes=[("Txt", "*.txt"), ("JPG", "*.jpg"), ("ENC", "*.enc")])
        message.configure(text=f"File name: {get_name()}"
                    if len(get_name()) < 30 else f"{get_type()} file chosen")
    except IndexError:
        messagebox.showinfo("Error","No file chosen!")


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

values = ["AES", "3DES", "Twofish"]
combo = Combobox(window, values=values, state='readonly')
combo.bind('<<ComboboxSelected>>', modified)
lbl4 = tk.Label(window, font=("Arial", 12), text="Choose an algorithm:")
empty = tk.Label(window)  # used for better look in GUI