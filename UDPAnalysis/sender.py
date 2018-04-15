import socket
import os
import datetime
import pickle
import time

BUF_SIZE = 1024
PORT = 3456


class Sender:
    def __init__(self, receiver_ip):
        self.__udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiver_ip = receiver_ip

        self.__tcp_socket.connect((self.receiver_ip, PORT))
        print("Connected to {}!".format(self.receiver_ip))

    def send_packets(self, n):
        send_time = datetime.datetime.now()
        print("Started sending packets")
        for i in range(1, n):
            data = bytearray(os.urandom(BUF_SIZE))
            bytes_sent = self.__udp_socket.sendto(data, (self.receiver_ip, PORT))

            time.sleep(0.5)

            tcp_data = pickle.dumps((send_time, bytes_sent))
            self.__tcp_socket.send(tcp_data)
        print("Packets successfully send. Elapsed time: {}.".format(datetime.datetime.now() - send_time))

    def close(self):
        self.__udp_socket.close()
        self.__tcp_socket.close()



