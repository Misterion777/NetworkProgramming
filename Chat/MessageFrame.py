import tkinter as tk


class MsgFrame(tk.Frame):
    def __init__(self, master, receiver, buttons_frame):
        tk.Frame.__init__(self, master)
        self.receiver = receiver
        self.master.current_receiver = self.receiver
        self.buttons_frame = buttons_frame

        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.msg_listbox = tk.Listbox(self, yscrollcommand=scrollbar.set, width=40, height=10)
        self.msg_listbox.pack()
        scrollbar.config(command=self.msg_listbox.yview)

        self.switch_button = tk.Button(buttons_frame, text=receiver, command=self.switch)
        self.switch_button.pack(side=tk.LEFT)

        self.buttons_push()

        self.grid(row=1, column=1, columnspan=3, sticky="nswe")
        self.master.receiver_frames_list.append(self)

    def buttons_push(self):
        for child in self.buttons_frame.winfo_children():
            child.configure(relief=tk.RAISED)
        self.switch_button.configure(relief=tk.SUNKEN)


    def switch(self):
        self.lift()
        self.master.current_receiver = self.receiver
        self.buttons_push()

    def close(self):
        self.master.receiver_frames_list.remove(self)
        self.switch_button.destroy()
        self.destroy()

    def insert(self, msg):
        self.msg_listbox.insert(tk.END, msg)
        self.msg_listbox.see(tk.END)
