import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from cryptography.fernet import Fernet

DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica", 15)
BUTTON_FONT = ("Helvetica", 13)
SMALL_FONT = ("Helvetica", 11)


#This key should be the same as the server's key
key = b'hB5IkGwJDELRrsRTc_ZonQNskKKP4Zaaec2dV4G1fxY='
cipher = Fernet(key)

class Client:
    def __init__(self, host='127.0.0.1', port=1234):
        self.host = host
        self.port = port

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

        self.root = tk.Tk()
        self.root.title("Chat Application (Client")
        self.root.geometry("500x500")
        self.root.resizable(False, False)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=4)
        self.root.grid_rowconfigure(2, weight=1)

        self.top_frame = tk.Frame(self.root, width=400, height=100, bg=DARK_GREY)
        self.top_frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.label = tk.Label(self.top_frame, text="Enter Username:", font=FONT, bg=DARK_GREY, fg=WHITE)
        self.label.pack(side=tk.LEFT, padx=10)

        self.username_entry = tk.Entry(self.top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE ,width=23)
        self.username_entry.pack(side=tk.LEFT)

        self.enter_button = tk.Button(self.top_frame, text="Join", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE ,command=self.set_username)
        self.enter_button.pack(side=tk.LEFT, padx=15)

        self.middle_frame = tk.Frame(self.root, width=400, height=700, bg=MEDIUM_GREY)
        self.middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

        self.chat_box = scrolledtext.ScrolledText(self.middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE , width=57,height=25)
        self.chat_box.pack()

        self.bottom_frame = tk.Frame(self.root, width=400, height=10, bg=DARK_GREY)
        self.bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

        self.message_entry = tk.Entry(self.bottom_frame, bg=MEDIUM_GREY, fg=WHITE, width=70 )
        self.message_entry.pack(side=tk.LEFT, padx=(10, 5), pady=(10, 10))

        self.send_button = tk.Button(self.bottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=(5, 10), pady=(10, 10))

        self.username = None
      
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)