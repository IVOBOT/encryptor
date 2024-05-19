import tkinter as tk
from tkinter import filedialog

def open_file():
    filepath = filedialog.askopenfilename(title="Wybierz plik do zaszyfrowania lub deszyfrowania")
    return filepath

open_file()
root = tk.Tk()
root.title("Szyfrowanie")
root.mainloop()