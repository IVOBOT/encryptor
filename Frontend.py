import tkinter as tk
from tkinter import filedialog
import os

def function(input_file, output_file, password):
    hash = ""
    asymmetric_key = ""
    symmetric_key = ""
    return hash, asymmetric_key, symmetric_key


class Frontend:
    input_file = None
    output_file = None
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
        # self.input_file = self.choose_input_file()
        self.init_window()
        self.draw_window_body()
        self.root.mainloop()

    def choose_input_file(self):
        if self.mode == "decrypt":
            self.input_file = filedialog.askopenfile(title="Choose input file", mode="rb", defaultextension=".enc", filetypes=[("Encrypted files", "*.enc"), ("All files", "*.*")])
        else:
            self.input_file = filedialog.askopenfile(title="Choose input file", mode="rb")
        

        for widget in self.left_sidebar.winfo_children():
            widget.destroy()
        self.left_sideba = self.draw_sidebar(side="left")

    def choose_output_file(self):
        if self.mode == "encrypt":
            self.output_file = filedialog.asksaveasfile(title="Choose output file", mode="wb", defaultextension=".enc", filetypes=[("Encrypted files", "*.enc"), ("All files", "*.*")])
        else:
            self.output_file = filedialog.asksaveasfile(title="Choose output file", mode="wb")
        
        for widget in self.right_sidebar.winfo_children():
            widget.destroy()
        self.right_sidebar = self.draw_sidebar(side="right")

    def update_view(self):
        self.output_file = None
        self.input_file = None
        for widget in self.frame_center.winfo_children():
            widget.destroy()
        self.draw_center_frame()
        for widget in self.left_sidebar.winfo_children():
            widget.destroy()
        self.left_sidebar = self.draw_sidebar(side="left")
        for widget in self.right_sidebar.winfo_children():
            widget.destroy()
        self.right_sidebar = self.draw_sidebar(side="right")
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
        file_menu.add_command(label="Choose input file", command=self.choose_input_file)
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
            choose_function = self.choose_input_file
            loaded_file = self.input_file
        elif side == "right":
            border_sticky = "ns"
            sticky = "nsew"
            column = 4
            grid_column = 3
            title = "OUTPUT FILE"
            choose_function = self.choose_output_file
            loaded_file = self.output_file
        else:
            return

        if loaded_file == None:
            descryption = "No file selected"
            file_icon_text = chr(0x1F5AE)  # question mark
        else:
            descryption = os.path.basename(loaded_file.name)
            extension = os.path.splitext(loaded_file.name)[1]
            if extension == '.enc':
                file_icon_text = chr(0x1F512)  # floppy disk
            elif extension in ['.txt', '.doc', '.docx', '.pdf']:
                file_icon_text = chr(0x1F4C4)  # file icon
            elif extension in ['.jpg', '.png', '.gif']:
                file_icon_text = chr(0x1F5BC)  # frame with picture
            elif extension in ['.mp3', '.wav']:
                file_icon_text = chr(0x1F3B6)  # musical notes
            elif extension in ['.mp4', '.avi']:
                file_icon_text = chr(0x1F39E)  # film frames
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
                if not self.password.get() or not self.input_file or not self.output_file:
                    tk.messagebox.showerror("Error", "Please fill all required fields")
                    return
                password = self.password.get()
                input_file = self.input_file
                output_file = self.output_file
                self.encrypt(password, input_file, output_file)
                input_file.close()
                output_file.close()
                tk.messagebox.showinfo("Encryption", "Encryption completed successfully")

            asymmetric_key = "PUBLIC KEY FOR SYMETRIC KEY ENCRYPTION"
            title = "ENCRYPT"
        elif self.mode == "decrypt":
            def function():
                if not self.password.get() or not self.input_file or not self.output_file:
                    tk.messagebox.showerror("Error", "Please fill all required fields")
                    return
                password = self.password.get()
                input_file = self.input_file
                output_file = self.output_file
                self.decrypt(password, input_file, output_file)
                input_file.close()
                output_file.close()
                tk.messagebox.showinfo("Decryption", "Decryption completed successfully")


            asymmetric_key = "PRIVATE KEY FOR SYMETRIC KEY DECRYPTION"
            title = "DECRYPT"
        else:
            return

        self.frame_center = tk.Frame(self.root, padx=10, pady=10, bg=self.center_color)
        self.frame_center.grid(row=0, column=2, sticky="nsew")

        password_entry = tk.Entry(self.frame_center, show="*", font="Helvetica 12 bold", textvariable=self.password)
        password_entry.pack(pady=5)

        '''hash_label = tk.Label(self.frame_center, text="HASH", fg="white", font="Helvetica 12 bold")
        hash_label.pack()

        hash_entry = tk.Entry(self.frame_center, textvariable=self.hash, state="disabled")
        hash_entry.pack(pady=5)

        public_key_label = tk.Label(self.frame_center, text=asymmetric_key, fg="white", font="Helvetica 12 bold")
        public_key_label.pack()

        public_key_entry = tk.Entry(self.frame_center, textvariable=self.asymmetric_key, state="disabled")
        public_key_entry.pack(pady=5)

        symmetric_key_label = tk.Label(self.frame_center, text="SYMMETRIC FILE ENCYPTION KEY", fg="white",
                                       font="Helvetica 12 bold")
        symmetric_key_label.pack()

        symmetric_key_entry = tk.Entry(self.frame_center, textvariable=self.symmetric_key, state="disabled")
        symmetric_key_entry.pack(pady=5)
        '''

        encrypt_button = tk.Button(self.frame_center, text=title, command=function, relief="flat",
                                   font="Helvetica 12 bold", bg=self.center_color)
        encrypt_button.pack(pady=10)

    def draw_window_body(self):
        self.left_sidebar = self.draw_sidebar(side="left")
        self.draw_center_frame()
        self.right_sidebar = self.draw_sidebar(side="right")
