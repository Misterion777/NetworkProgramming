import tkinter as tk
import socket, pickle
from threading import Thread
import Chat.TopLevels as top
import Chat.MessageFrame as msg
import Chat.Server as serv
from tkinter import messagebox
import time


ALL = "All"
PORT = 50000


class MainFrame(tk.Frame):
    def __init__(self, master, controller):

        tk.Frame.__init__(self, master)
        self.controller = controller
        self.current_receiver = ALL
        self.receiver_frames_list = []

        tk.Label(self, text='Current users:').grid(row=0, column=0, sticky='w')
        self.users_listbox = tk.Listbox(self, height=9)
        self.users_listbox.bind('<Double-Button-1>', self.create_dm_frame)
        self.users_listbox.grid(row=1, column=0, sticky="nswe")

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.grid(row=0, column=1, sticky='w')

        msg.MsgFrame(self, ALL, self.buttons_frame)

        self.msg_entry = tk.Entry(self)
        self.msg_entry.grid(row=2, column=0, columnspan=4, sticky='wsen')
        self.msg_entry.bind('<Return>', lambda event: self.click_send(self.msg_entry.get()))

        self.ip_label = tk.Label(self, text=self.controller.server_ip)
        self.ip_label.grid(row=3, column=1, columnspan=2, sticky='wsen')

        tk.Button(self, text='Send', command=lambda: self.click_send(self.msg_entry.get())).grid(row=3,
                                                                                                 column=3,
                                                                                                 sticky='e')

        tk.Button(self, text='History', command=self.click_history).grid(row=3,
                                                                                                 column=0,
                                                                                                 sticky='w')
        self.grid(row=0, column=0, sticky="nsew")

        self.msg_entry.focus_set()
        self.controller.protocol("WM_DELETE_WINDOW", self.on_close)

        Thread(target=self.recieve).start()

    def click_history(self):
        self.history_top = top.HistoryTopLevel(self, self.controller)


    def set_state(self, state):
        for child in self.winfo_children():
            try:
                child.configure(state=state)
            except tk.TclError:
                pass


    def create_dm_frame(self, event=None):
        user = self.users_listbox.get(self.users_listbox.curselection())
        for item in self.receiver_frames_list:
            if user == item.receiver or user == self.controller.client_name:
                return
        msg.MsgFrame(self, user, self.buttons_frame)

    def click_send(self, msg, event=None):
        data = pickle.dumps((self.current_receiver, msg))
        try:
            self.controller.client_socket.send(data)
        except BrokenPipeError:
            messagebox.showerror("Host Error", "Connection with the host lost!")
            self.controller.close()
        self.msg_entry.delete(0, tk.END)

    def recieve(self):
        while True:
            try:
                try:
                    (sender, data) = pickle.loads(self.controller.client_socket.recv(1024))
                    if sender == "$history$":
                        self.history_top.fill_listbox(data)
                    elif sender == "sys":
                        self.update_users_list(data)
                        self.update_users_frames(data)
                    else:
                        frame_exists = False
                        for frame in self.receiver_frames_list:
                            if sender == frame.receiver:
                                frame.insert(data)
                                frame_exists = True
                                break
                        if not frame_exists:
                            msg.MsgFrame(self, sender, self.buttons_frame).insert(data)
                except EOFError:
                    pass
            except OSError:
                break

    def update_users_list(self, users_list):
        self.users_listbox.delete(0, tk.END)
        for user in users_list:
            self.users_listbox.insert(tk.END, user)

    def update_users_frames(self, users_list):
        frame_was_closed = False
        for frame in self.receiver_frames_list:
            if frame.receiver not in users_list and frame.receiver != ALL:
                frame.close()
                frame_was_closed = True
        if frame_was_closed:
            self.receiver_frames_list[-1].switch()

    def on_close(self):
        data = pickle.dumps(("sys", "$quit$"))
        self.controller.client_socket.send(data)
        self.controller.close()


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("Chat")

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_name = ""
        self.server_ip = ""
        self.server = serv.Server()

        # Window startup customization
        self.x = (self.winfo_screenwidth() - self.winfo_reqwidth()) / 2
        self.y = (self.winfo_screenheight() - self.winfo_reqheight()) / 3
        self.geometry("+%d+%d" % (self.x, self.y))

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.mod_switcher = ModeSwitcher(self.container, self)
        self.mod_switcher.wait_window()
        self.main_frame = MainFrame(self.container, self)

    def host(self):
        self.mod_switcher.destroy()
        self.server.start_server()
        self.connect(serv.ADDRESS)
        top.Authorization(self.container, self, "Register", "Please enter your nickname: ").wait_window()

    def client(self):
        self.mod_switcher.destroy()
        top.AddressInput(self.container, self, "Host address", "Please enter host IP: ").wait_window()
        top.Authorization(self.container, self, "Register", "Please enter your nickname: ").wait_window()

    def connect(self, host):
        addr = (host, PORT)
        self.server_ip = host
        self.client_socket.connect(addr)

    def close(self):
        self.client_socket.close()
        self.server.close()
        print('Client turn off!\n')
        self.destroy()

    def set_coords(self, widget):
        widget.geometry("+%d+%d" % (self.x, self.y))
        widget.attributes('-topmost', 'true')


class ModeSwitcher(tk.Toplevel):
    def __init__(self, master, controller ):
        tk.Toplevel.__init__(self, master)

        self.controller = controller
        self.resizable(False, False)
        self.transient(self.master)

        self.title("Chat")
        tk.Button(self, text="HOST LOBBY", command=self.controller.host, width=10, height=2).pack(pady=3, padx=20)
        tk.Button(self, text="JOIN LOBBY", command=self.controller.client, width=10, height=2).pack(pady=3)
        tk.Button(self, text="EXIT", command=self.controller.close, width=10, height=2).pack(pady=15)


        self.controller.set_coords(self)


        self.protocol("WM_DELETE_WINDOW", self.controller.close)



if __name__ == '__main__':
    app = App()
    app.mainloop()

