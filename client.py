import socket
import threading
from tkinter import *
from tkinter import simpledialog
from tkinter.scrolledtext import ScrolledText

host = "127.0.0.1"
port = 8080

class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = Tk()
        msg.withdraw()
        
        self.nickname = simpledialog.askstring("ASSCord", "Choose your username:", parent=msg)
        
        self.gui_done = False

        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.root = Tk()
        self.root.configure(bg="#1f2340")
        self.root.title(f"ASSCord: {self.nickname}")

        self.chatLabel = Label(self.root, text="ASSCord:", bg="#1f2340", fg="green",font=("Ariel", 20), anchor=CENTER).pack(pady=5)

        self.messages = ScrolledText(self.root, state="disabled")
        self.messages.pack(pady=10)

        self.messageLabel = Label(self.root, text="Message:", bg="#1f2340", fg="green", font=("Ariel", 20), anchor=CENTER).pack(pady=5)

        self.messageInput = Entry(self.root, width=50)
        self.messageInput.pack()

        self.button = Button(self.root, text="Send", command=self.send).pack(pady=5)

        self.gui_done = True

        self.root.protocol("WM_DELETE_WINDOW", self.stop)

        message = f"\n{self.nickname}"
        self.sock.send(message.encode("utf-8"))

        self.root.mainloop()

    def send(self):
        message = f"{self.nickname}: {self.messageInput.get()}"
        self.sock.send(message.encode("utf-8"))
        self.messageInput.delete(0, "end")

    def stop(self):
        self.running = False
        self.root.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode("utf-8")
                if message == "NICK":
                    self.sock.send(self.nickname.encode("utf-8"))
                else:
                    if self.gui_done:
                        self.messages.config(state="normal")
                        self.messages.insert("end", ((f"{message}\n").replace("b'", "")).replace("'", ""))
                        self.messages.yview("end")
                        self.messages.config(state="disabled")
            except ConnectionAbortedError:
                break
            except:
                print("\nError Occured.\nClosing Server...\n")
                self.sock.close()
                break

client = Client(host, port)