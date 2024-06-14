import tkinter as tk
from tkinter import filedialog
import os

def function(input_file, output_file, password):
    hash = ""
    asymmetric_key = ""
    symmetric_key = ""
    return hash, asymmetric_key, symmetric_key


class Frontend:
    output_filename = None
    input_filename = None
    password = None
    hash = None
    asymmetric_key = None
    symmetric_key = None
    root = None
    frame_center = None
    left_sidebar = None
    right_sidebar = None
    encrypt = None
    decrypt = None
    mode = "encrypt"

    center_color = "#323232"
    sidebar_color = "#444444"
    sidebar_border_color = "#777777"

    def __init__(self, encryption_function, decryption_function):
        self.encrypt = encryption_function
        self.decrypt = decryption_function
        self.choose_input_filename()
        self.init_window()
        self.draw_window_body()
        self.root.mainloop()

    def reset_sidebars(self):
        if (self.left_sidebar is not None):
            for widget in self.left_sidebar.winfo_children():
                widget.destroy()
            self.left_sidebar = self.draw_sidebar(side="left")
        if (self.right_sidebar is not None):
            for widget in self.right_sidebar.winfo_children():
                widget.destroy()
            self.right_sidebar = self.draw_sidebar(side="right")

    def choose_input_filename(self):
        if self.mode == "decrypt":
            self.input_filename = filedialog.askopenfilename(
                title="Choose input file",
                defaultextension=".enc",
                filetypes=[("Encrypted files", "*.enc"), ("All files", "*.*")],
                initialdir="~/Desktop"
            )
            if self.input_filename == "":
                self.input_filename = None
                self.output_filename = None
                self.reset_sidebars()
                return
            self.output_filename = self.input_filename.split(".")[0]
        elif self.mode == "encrypt":
            self.input_filename = filedialog.askopenfilename(
                title="Choose input file",
                initialdir="~/Desktop"
            )
            if self.input_filename == "":
                self.input_filename = None
                self.output_filename = None
                self.reset_sidebars()
                return
            self.output_filename = self.input_filename.split(".")[0] + ".enc"
        else:
            raise ValueError("Invalid mode")
        self.reset_sidebars()

    def choose_output_filename(self):
        if self.mode == "encrypt":
            self.output_filename = filedialog.asksaveasfilename(
                title="Choose output file",
                defaultextension=".enc",
                filetypes=[("Encrypted files", "*.enc"), ("All files", "*.*")],
                initialdir="~/Desktop"
            )
        if self.output_filename == "":
            self.output_filename = None
            return
        else:
            self.output_filename = filedialog.asksaveasfilename(
                title="Choose output file",
                initialdir="~/Desktop"
            )
        self.reset_sidebars()

    def update_view(self):
        self.output_filename = None
        self.input_filename = None
        for widget in self.frame_center.winfo_children():
            widget.destroy()
        self.draw_center_frame()
        self.reset_sidebars()
        self.root.update_idletasks()

    def set_mode_encrypt(self):
        self.mode = "encrypt"
        self.root.title("Encryption Tool")
        self.update_view()

    def set_mode_decrypt(self):
        self.mode = "decrypt"
        self.root.title("Decryption Tool")
        self.update_view()

    def init_window(self):
        self.root = tk.Tk()
        self.password = tk.StringVar()
        self.hash = tk.StringVar()
        self.asymmetric_key = tk.StringVar()
        self.symmetric_key = tk.StringVar()
        self.root.title("Encryption Tool")
        self.root.resizable(False, False)

        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Choose input file", command=self.choose_input_filename)
        file_menu.add_separator()
        file_menu.add_command(label="Close app", command=self.root.quit)

        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Encrypt", command=self.set_mode_encrypt)
        edit_menu.add_command(label="Decrypt", command=self.set_mode_decrypt)

    def draw_sidebar(self, side):
        if side == "left":
            border_sticky = "nsew"
            sticky = "ns"
            column = 0
            grid_column = 1
            title = "INPUT FILE"
            choose_function = self.choose_input_filename
            loaded_filename = self.input_filename
        elif side == "right":
            border_sticky = "ns"
            sticky = "nsew"
            column = 4
            grid_column = 3
            title = "OUTPUT FILE"
            choose_function = self.choose_output_filename
            loaded_filename = self.output_filename
        else:
            raise ValueError("Invalid side")
        if loaded_filename == None or loaded_filename == "":
            descryption = "No file selected"
            file_icon_text = chr(0x1F5AE)  # question mark
        else:
            descryption = loaded_filename.split("/")[-1]
            extension = loaded_filename.split(".")[-1]
            if extension == 'enc':
                file_icon_text = chr(0x1F512)  # floppy disk
            elif extension in ['txt', 'doc', 'docx', 'pdf']:
                file_icon_text = chr(0x1F4C4)  # file icon
            elif extension in ['jpg', 'png', 'gif']:
                file_icon_text = chr(0x1F5BC)  # frame with picture
            elif extension in ['mp3', 'wav']:
                file_icon_text = chr(0x1F3B6)  # musical notes
            elif extension in ['mp4', 'avi']:
                file_icon_text = chr(0x1F39E)  # film frames
            elif extension in ['zip', 'rar', '7z']:
                file_icon_text = chr(0x1F4E6)
            elif extension in ['<?>']:
                file_icon_text = chr(0x1F5C2)
            else:
                file_icon_text = chr(0x1F5C2)  # file folder


        sidebar_frame = tk.Frame(self.root, padx=20, pady=10, bg=self.sidebar_color)
        sidebar_frame.grid(row=0, column=column, sticky=border_sticky)

        sidebar_frame_border = tk.Frame(self.root, bg=self.sidebar_border_color, width=1)
        sidebar_frame_border.grid(row=0, column=grid_column, sticky=sticky)

        file_label = tk.Label(sidebar_frame, text=title, fg="white", font="Helvetica 12 bold", bg=self.sidebar_color)
        file_label.pack(anchor="n")

        file_icon = tk.Label(sidebar_frame, text=file_icon_text, font="Helvetica 120", bg=self.sidebar_color)
        file_icon.pack(pady=10)

        file_description = tk.Label(sidebar_frame, text=descryption, font="Helvetica 12 bold", bg=self.sidebar_color)
        file_description.pack(pady=5)

        file_button_frame = tk.Frame(sidebar_frame, width=10, height=30)
        file_button_frame.pack(pady=5)

        choose_file_button = tk.Button(file_button_frame, text="CHOOSE", command=choose_function,
                                       font="Helvetica 12 bold", bg=self.sidebar_color, bd=0, highlightthickness=0,
                                       relief='flat')
        choose_file_button.pack(fill="both", expand=True)

        return sidebar_frame

    def draw_center_frame(self):
        if self.mode == "encrypt":
            def function():
                if not self.password.get() or not self.input_filename:
                    tk.messagebox.showerror("Error", "Please fill all required fields")
                    return
                password = self.password.get()
                self.encrypt(password, self.input_filename, self.output_filename)
                tk.messagebox.showinfo("Encryption", "Encryption completed successfully")

            asymmetric_key = "PUBLIC KEY FOR SYMETRIC KEY ENCRYPTION"
            title = "ENCRYPT"
        elif self.mode == "decrypt":
            def function():
                if not self.password.get() or not self.input_filename:
                    tk.messagebox.showerror("Error", "Please fill all required fields")
                    return
                password = self.password.get()
                self.decrypt(password, self.input_filename, self.output_filename)
                tk.messagebox.showinfo("Decryption", "Decryption completed successfully")

            asymmetric_key = "PRIVATE KEY FOR SYMETRIC KEY DECRYPTION"
            title = "DECRYPT"
        else:
            return

        self.frame_center = tk.Frame(self.root, padx=10, pady=10, bg=self.center_color)
        self.frame_center.grid(row=0, column=2, sticky="nsew")

        # Dodanie niewidzialnego Frame na górze dla centrowania
        tk.Frame(self.frame_center, height=1, bg=self.center_color).pack(side="top", expand=True)

        password_entry = tk.Entry(self.frame_center, show="*", font="Helvetica 12 bold", textvariable=self.password)
        password_entry.pack(pady=5)

        encrypt_button = tk.Button(self.frame_center, text=title, command=function, relief="flat",
                                font="Helvetica 12 bold", bg=self.center_color)
        encrypt_button.pack(pady=10)

        # Dodanie niewidzialnego Frame na dole dla centrowania
        tk.Frame(self.frame_center, height=1, bg=self.center_color).pack(side="bottom", expand=True)

    def draw_window_body(self):
        self.left_sidebar = self.draw_sidebar(side="left")
        self.draw_center_frame()
        self.right_sidebar = self.draw_sidebar(side="right")
