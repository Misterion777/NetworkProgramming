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

    def send_packets(self, n):

        print("Started sending packets")
        for i in range(n):
            data = bytearray(os.urandom(BUF_SIZE))
            self.__udp_socket.sendto(data, (self.receiver_ip, PORT))

        self.__tcp_socket.connect((self.receiver_ip, PORT))
        self.__tcp_socket.send((n).to_bytes(10,byteorder='big'))

    def close(self):
        self.__udp_socket.close()
        self.__tcp_socket.close()



