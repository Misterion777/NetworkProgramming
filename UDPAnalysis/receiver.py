import socket
import datetime
import pickle

BUF_SIZE = 1024
PORT = 3456


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


class Receiver:
    def __init__(self):
        timeout = 20
        self.__udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.__udp_socket.settimeout(timeout)

        self.__tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = get_ip()

        self.__tcp_socket.bind((self.ip, PORT))
        self.__tcp_socket.listen(5)
        self.__sender_socket = socket.socket()
        print("Successfully created sockets. Current IP: {}".format(self.ip))

        self.__accept_connection()

    def __accept_connection(self):
        print("Waiting for connection of sender...")
        self.__sender_socket, sender_address = self.__tcp_socket.accept()
        print("{} connected!".format(sender_address))

    def receive_packets(self):
        packets_total = 0
        bytes_send_total = 0
        received_bytes = 0
        send_time = datetime.datetime(1, 1, 1)
        receive_time = datetime.datetime(1, 1, 1)
        print("Started receiving packets!")
        while True:
            try:
                received_bytes, sender_ip = self.__udp_socket.recvfrom(BUF_SIZE)
                receive_time = datetime.datetime.now()

                (send_time, bytes_sent) = pickle.loads(self.__sender_socket.recv(BUF_SIZE))
                bytes_send_total += bytes_sent
                received_bytes += len(received_bytes)
                packets_total += 1
            except socket.timeout:
                speed = self.__count_time(receive_time, send_time)
                loss = self.__count_loss(bytes_send_total, received_bytes)
                print("Total packets received: {}".format(packets_total))
                print("Data loss: {}%. Connection speed: {}".format(loss, speed))
                break

    @staticmethod
    def __count_time(receive_time, send_time):
        return send_time - receive_time

    @staticmethod
    def __count_loss(bytes_sent, received_bytes):
        return (1 - (received_bytes / bytes_sent)) * 100

    def close(self):
        self.__udp_socket.close()
        self.__tcp_socket.close()