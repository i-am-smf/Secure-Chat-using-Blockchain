import socket
import threading
import tkinter as tk
from tkinter import simpledialog,messagebox

class Client:
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:

            self.client.connect((host, port))
        except:
            self.nickname = messagebox.showwarning(title="Not Found",message="The server don't response to the client system")
            return

        self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname:")
        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.window = tk.Tk()
        self.window.configure(bg="#3498db")

        self.chat_box = tk.Text(self.window, height=20, width=50, bg="#2980b9", fg="white",state="disabled")
        self.chat_box.pack(padx=10, pady=10)
        self.message_entry = tk.Entry(self.window, width=30)
        self.message_entry.pack(padx=10, pady=10)
        self.message_entry.bind("<Return>", self.send)

        self.send_button = tk.Button(self.window, text="Send", command=self.send)
        self.send_button.pack(padx=10, pady=10)

        self.gui_done = True

        self.window.protocol("WM_DELETE_WINDOW", self.stop)

        self.window.mainloop()

    def send(self, event=None):
        message = self.message_entry.get()
        message = f"{self.nickname}: {message}"
        self.client.send(message.encode('utf-8'))
        self.message_entry.delete(0, tk.END)

    def receive(self):
        while self.running:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.chat_box.config(state=tk.NORMAL)
                        
                        self.chat_box.insert(tk.END, message + '\n')
                        self.chat_box.config(state=tk.DISABLED)
                        self.chat_box.see(tk.END)
            except Exception as e:
                print(f"Error: {e}")
                self.running = False

    def stop(self):
        self.running = False
        self.client.close()
        self.window.destroy()

# Start the client
client = Client('127.0.0.1', 5555)
