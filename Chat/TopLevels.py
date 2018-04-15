import tkinter as tk
from tkinter import messagebox as msg
import platform
import pickle


class HistoryTopLevel(tk.Toplevel):
    def __init__(self, master, controller):
        tk.Toplevel.__init__(self, master)
        self.controller = controller
        self.resizable(False, False)
        self.title('History')
        
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox = tk.Listbox(self, yscrollcommand=scrollbar.set, width=40, height=10)
        self.listbox.pack()
        scrollbar.config(command=self.listbox.yview)
        self.send_request()
        self.controller.set_coords(self)
    
    def send_request(self):
        request = pickle.dumps(('all', '$history$'))
        self.controller.client_socket.send(request)


    def fill_listbox(self, data):
        self.listbox.delete(0, tk.END)
        for line in data:
            self.listbox.insert(tk.END, line)






class IntroTopLevel(tk.Toplevel):
    def __init__(self, master, controller, title, label_text):
        tk.Toplevel.__init__(self, master)

        self.controller = controller
        self.resizable(False, False)
        self.transient(self.master)

        self.title(title)
        tk.Label(self, text=label_text).pack(anchor='w')
        self.addr_input = tk.Entry(self)
        self.addr_input.pack(fill='x')
        self.addr_input.focus_set()
        self.set_entry()
        button_frame = tk.Frame(self)
        tk.Button(button_frame, text='Cancel', command=self.controller.close).pack(side='right')
        tk.Button(button_frame, text='Ok', command=lambda: self.click_ok(self.addr_input.get())).pack(side='right')
        button_frame.pack(anchor='e')

        self.bind('<Return>', lambda event: self.click_ok(self.addr_input.get()))

        self.controller.set_coords(self)

        self.protocol("WM_DELETE_WINDOW", self.controller.close)

    def click_ok(self, data, event=None):
        pass

    def set_entry(self):
        pass


class AddressInput(IntroTopLevel):
    def click_ok(self, address, event=None):
        try:
            self.controller.connect(address)
            self.destroy()
        except TimeoutError:
            msg.showerror("Timeout!",
                          "Connection attempt failed because the connected party"
                          " did not properly respond after a period of time", parent=self)
        except OSError:
            msg.showerror("Error!", "No Route to host", parent=self)


class Authorization(IntroTopLevel):
    def click_ok(self, name, event=None):
        self.controller.client_socket.send(bytes(name, "utf-8"))
        self.controller.client_name = name
        self.destroy()

    def set_entry(self):
        self.addr_input.insert(0, platform.node())





