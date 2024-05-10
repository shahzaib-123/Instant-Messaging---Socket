import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Instant Messenger")
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "18.234.155.211" #IP of server here
        self.port = 80
        self.sock.connect((self.host, self.port))
        
        # GUI layout
        self.text_area = scrolledtext.ScrolledText(master, state='disabled')
        self.text_area.grid(row=0, column=0, columnspan=2)
        
        self.msg_entry = tk.Entry(master)
        self.msg_entry.grid(row=1, column=0)
        
        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1)
        
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self):
        message = self.msg_entry.get()
        if message:
            self.sock.sendall(message.encode())
            self.msg_entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                message = self.sock.recv(1024).decode()
                if message:
                    self.display_message(message)
            except:
                messagebox.showinfo("Disconnected", "You have been disconnected from the server.")
                self.sock.close()
                break

    def display_message(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.yview(tk.END)
        self.text_area.config(state='disabled')

def main():
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()

if __name__ == "__main__":
    main()
