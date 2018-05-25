import socket
from threading import Thread, Condition
import pickle
import time
import Chat.history as history

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

ALL = "All"
PORT = 50000
ADDRESS = get_ip()

class Server():
    def __init__(self):
        self.clients = {}
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.history = history.History()

    def start_server(self):
        self.s.bind((ADDRESS, PORT))
        self.s.listen(10)
        print('in process...')
        server_thread = Thread(target=self.accept_connections)
        server_thread.daemon = True
        server_thread.start()

    def close(self):
        self.s.close()

    def accept_connections(self):
        while True:
            try:
                client_socket, client_addr = self.s.accept()
            except OSError:
                self.s.close()
                print('Server turn off!')
                break
            print('accepted connection')
            Thread(target=self.handle_client, args=(client_socket,)).start()


    def handle_client(self, client_socket):

        name = client_socket.recv(1024).decode("utf-8")

        self.clients[name] = client_socket
        self.broadcast(name, " has joined the chat!")

        print(name + " connected")

        self.update_users_list()
        while True:
            (receiver, msg) = pickle.loads(client_socket.recv(1024))
            if msg == "$quit$":
                client_socket.close()
                del self.clients[name]
                self.broadcast(name, " has left the chat!")
                self.update_users_list()
                print(name + ' disconnected')
                break
            elif msg == '$history$':  
                self.send_history(client_socket, name)
            elif receiver == ALL:
                self.broadcast(name, ": " + msg)
            else:
                self.direct_message(receiver, name, msg)

    def send_history(self, client_socket, name):
        data = pickle.dumps(('$history$', self.history.read_from_file(name)))
        client_socket.send(data)

    def update_users_list(self):
        dumped_list = list(self.clients.keys())
        data = pickle.dumps(("sys", dumped_list))
        time.sleep(0.5)
        for socket in self.clients.values():
            socket.send(data)


    def direct_message(self, receiver, sender, msg):
        string_value = "{}: {}".format(sender, msg)
        self.history.write_to_file(sender, receiver, string_value)

        data_for_receiver = pickle.dumps((sender, string_value))
        data_for_sender = pickle.dumps((receiver, string_value))
        self.clients[receiver].send(data_for_receiver)
        self.clients[sender].send(data_for_sender)


    def broadcast(self, name, msg):
        string_value = "{}{}".format(name, msg)
        self.history.write_to_file(ALL, ALL, string_value)

        data = pickle.dumps((ALL, string_value))
        for socket in self.clients.values():
            socket.send(data)



