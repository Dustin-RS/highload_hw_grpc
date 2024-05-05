import threading
from tkinter import *
from tkinter import simpledialog

import grpc

import chat_pb2 as chat__pb2
import chat_pb2_grpc as rpc

address = 'localhost'
port = 8080


class Client:
    def __init__(self, u: str, window):
        self.window = window
        self.username = u
        channel = grpc.insecure_channel(address + ':' + str(port))
        self.conn = rpc.ChatServiceStub(channel)
        threading.Thread(target=self.__listen_for_messages, daemon=True).start()
        self.__setup_ui()
        self.window.mainloop()

    def __listen_for_messages(self):
        """
        Function for separate thread for receiving messages
        """
        for message in self.conn.ChatStream(chat__pb2.Empty()):
            print(f"Received from [{message.username}]: {message.message}")
            self.chat_list.insert(END, f"[{message.username}] {message.message}\n")

    def send_message(self, event):
        message = self.entry_message.get()
        if message is not '':
            n = chat__pb2.Message()
            n.username = self.username
            n.message = message
            print(f"Sent from [{n.username}]: {n.message}")
            self.conn.SendMessage(n)

    def __setup_ui(self):
        self.chat_list = Text()
        self.chat_list.pack(side=TOP)
        self.lbl_username = Label(self.window, text=self.username)
        self.lbl_username.pack(side=LEFT)
        self.entry_message = Entry(self.window, bd=5)
        self.entry_message.bind('<Return>', self.send_message)
        self.entry_message.focus()
        self.entry_message.pack(side=BOTTOM)


if __name__ == '__main__':
    root = Tk()
    frame = Frame(root, width=400, height=400)
    frame.pack()
    root.withdraw()
    username = None
    while username is None:
        username = simpledialog.askstring("Username", "What's your username?", parent=root)
    root.deiconify()
    c = Client(username, frame)
