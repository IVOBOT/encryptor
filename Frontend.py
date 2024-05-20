import tkinter as tk
from tkinter import filedialog

class Frontend:

    input_file = None
    output_file = None
    password = None

    def __init__(self):
        self.input_file = self.choose_input_file()
        root = self.init_window()
        self.draw_window_body(root)
        root.mainloop()

    def choose_input_file(self):
        self.input_file = filedialog.askopenfile(title="Choose input file")

    def choose_output_file(self):
        self.output_file = filedialog.asksaveasfile(title="Choose output file")

    def init_window(self):
        root = tk.Tk()
        root.title("Encryption Tool")
        root.resizable(False, False)

        menubar = tk.Menu(root)
        root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Choose input file", command=self.choose_input_file)
        file_menu.add_separator()
        file_menu.add_command(label="Close app", command=root.quit)

        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Encrypt")
        edit_menu.add_command(label="Decrypt")

        return root

    def draw_window_body(self, root):
        frame_left = tk.Frame(root, padx=10, pady=10)
        frame_left.grid(row=0, column=0, sticky="nsew")

        frame_left_border = tk.Frame(root, bg="black", width=2)
        frame_left_border.grid(row=0, column=1, sticky="ns")

        frame_center = tk.Frame(root, padx=10, pady=10)
        frame_center.grid(row=0, column=2, sticky="nsew")

        frame_right_border = tk.Frame(root, bg="black", width=2)
        frame_right_border.grid(row=0, column=3, sticky="ns")

        frame_right = tk.Frame(root, padx=10, pady=10)
        frame_right.grid(row=0, column=4, sticky="nsew")
        root.columnconfigure(1, weight=1)

        file_input_label = tk.Label(frame_left, text="INPUT FILE", fg="white", font="Helvetica 12 bold")
        file_input_label.pack(anchor="n")

        file_input_icon = tk.Label(frame_left, text=chr(0x1F4C4), relief="flat", font = "Helvetica 120")
        file_input_icon.pack(pady=10)

        file_input_description = tk.Label(frame_left, text="No file selected", font="Helvetica 12 bold")
        file_input_description.pack(pady=5)
        
        choose_input_button = tk.Button(frame_left, text="CHOOSE", command=self.choose_input_file, relief="flat", font="Helvetica 12 bold")
        choose_input_button.pack(pady=10)

        password_label = tk.Label(frame_center, text="PASSWORD", fg="white", font="Helvetica 12 bold")
        password_label.pack()

        password_entry = tk.Entry(frame_center)
        password_entry.pack(pady=5)

        hash_label = tk.Label(frame_center, text="HASH", fg="white", font="Helvetica 12 bold")
        hash_label.pack()

        hash_entry = tk.Entry(frame_center)
        hash_entry.pack(pady=5)

        public_key_label = tk.Label(frame_center, text="PUBLIC KEY FOR SYMMETRIC KEY ENCRYPTION", fg="white", font="Helvetica 12 bold")
        public_key_label.pack()

        public_key_entry = tk.Entry(frame_center)
        public_key_entry.pack(pady=5)

        symmetric_key_label = tk.Label(frame_center, text="SYMMETRIC FILE ENCYPTION KEY", fg="white", font="Helvetica 12 bold")
        symmetric_key_label.pack()

        symmetric_key_entry = tk.Entry(frame_center)
        symmetric_key_entry.pack(pady=5)

        encrypt_button = tk.Button(frame_center, text="ENCRYPT", command=self.choose_output_file, relief="flat", font="Helvetica 12 bold")
        encrypt_button.pack(pady=10)

        file_output_label = tk.Label(frame_right, text="OUTPUT FILE", fg="white", font="Helvetica 12 bold")
        file_output_label.pack(anchor="n")

        file_output_icon = tk.Label(frame_right, text=chr(0x1F4C4), relief="flat", font = "Helvetica 120")
        file_output_icon.pack(pady=10)

        file_output_description = tk.Label(frame_right, text="No file selected", font="Helvetica 12 bold")
        file_output_description.pack(pady=5)
        
        choose_output_button = tk.Button(frame_right, text="CHOOSE", command=self.choose_output_file, relief="flat", font="Helvetica 12 bold")
        choose_output_button.pack(pady=10)