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

    def handle_client(self, client_socket, addr):
        self.client_list.insert(tk.END, f"Client {addr} connected\n")
        self.client_list.yview(tk.END)

        # Inform the new client of existing clients
        for client in self.clients:
            if client['socket'] != client_socket:
                client_socket.send(cipher.encrypt(f"{client['username']} is already in the chat".encode('utf-8')))

        while True:
            try:
                msg = client_socket.recv(1024)
                if msg:
                    decrypted_msg = cipher.decrypt(msg).decode('utf-8')
                    if decrypted_msg.startswith('NEWUSER:'):
                        username = decrypted_msg.split(':')[1]
                        for client in self.clients:
                            if client['socket'] == client_socket:
                                client['username'] = username
                        self.broadcast(f"{username} has joined the chat", sender=client_socket)
                    else:
                        self.messages.insert(tk.END, decrypted_msg + "\n")
                        self.messages.yview(tk.END)
                        self.broadcast(decrypted_msg, sender=client_socket)
                        
            except Exception as e:
                username = None
                for client in self.clients:
                    if client['socket'] == client_socket:
                        username = client['username']
                        break
                if username:
                    self.broadcast(f"{username} has left the chat", sender=client_socket)
                client_socket.close()
                self.clients = [c for c in self.clients if c['socket'] != client_socket]
                self.client_list.insert(tk.END, f"Client {addr} disconnected\n")
                self.client_list.yview(tk.END)
                break

    def accept_clients(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            self.clients.append({'socket': client_socket, 'address': addr, 'username': None})
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
            client_thread.start()

    def run(self):
        server_thread = threading.Thread(target=self.accept_clients)
        server_thread.start()
        self.root.mainloop()

if __name__ == "__main__":
    server = Server()
    server.run()
