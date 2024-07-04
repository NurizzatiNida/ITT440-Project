import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from cryptography.fernet import Fernet

DARK_GREY = '#121212'
WHITE = "white"
MEDIUM_GREY = '#1F1B24'
FONT = ("Helvetica", 12)

# Generate a key for encryption/decryption
key = b'hB5IkGwJDELRrsRTc_ZonQNskKKP4Zaaec2dV4G1fxY='
cipher = Fernet(key)

class Server:
    def __init__(self, host='127.0.0.1', port=1234):
        self.clients = []
        self.host = host
        self.port = port

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(3)

        self.root = tk.Tk()
        self.root.title("Chat Application (Server)")

        self.top_frame = tk.Frame(self.root, bg=DARK_GREY)
        self.top_frame.pack()

        self.label = tk.Label(self.top_frame, text="Clients Connected:", font=FONT, bg=DARK_GREY, fg=WHITE)
        self.label.pack()

        self.client_list = scrolledtext.ScrolledText(self.top_frame, height=5, font=FONT,fg=WHITE, bg=MEDIUM_GREY)
        self.client_list.pack()

        self.label = tk.Label(self.top_frame, text="Clients Messages:", font=FONT, bg=DARK_GREY, fg=WHITE)
        self.label.pack()

        self.bottom_frame = tk.Frame(self.root, bg=DARK_GREY)
        self.bottom_frame.pack()

        self.messages = scrolledtext.ScrolledText(self.bottom_frame, height=10, font=FONT,fg=WHITE, bg=MEDIUM_GREY)
        self.messages.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        for client in self.clients:
            client['socket'].close()
        self.server_socket.close()
        self.root.destroy()

    def broadcast(self, msg, sender=None):
        for client in self.clients:
            if client['socket'] != sender:
                try:
                    encrypted_msg = cipher.encrypt(msg.encode('utf-8'))
                    client['socket'].send(encrypted_msg)
                except Exception as e:
                    client['socket'].close()
                    self.clients.remove(client)
                    self.client_list.insert(tk.END, f"Client {client['address']} disconnected\n")
                    self.client_list.yview(tk.END)