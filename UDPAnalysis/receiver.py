import socket
import datetime
from threading import Thread

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

        self.__udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.__tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.ip = get_ip()
        self.address = (self.ip, PORT)

        self.__udp_socket.bind(self.address)
        self.__tcp_socket.bind(self.address)
        self.__tcp_socket.listen(5)
        print("Successfully created sockets. Current IP: {}".format(self.ip))

        self.udpConnected = True
        self.packets_sent = 0

    def listen_tcp(self):
        sender_socket, sender_address = self.__tcp_socket.accept()
        self.packets_sent = int.from_bytes(sender_socket.recv(10), byteorder='big')
        self.udpConnected = False
        try:
            self.__udp_socket.shutdown(socket.SHUT_RD)
        except OSError:
            print("Packets receiving finished!")

    def receive_packets(self):
        tcp_thread = Thread(target=self.listen_tcp)
        tcp_thread.start()

        self.udpConnected = True
        packets_received = 0
        print("Started receiving packets!")
        start_time = datetime.datetime.now()
        while True:
            self.__udp_socket.recv(BUF_SIZE)
            if not self.udpConnected:
                break
            packets_received += 1

        finish_time = datetime.datetime.now()
        print("Packets sent:{} \nPackets received: {}".format(self.packets_sent, packets_received))
        print("Speed: {} packets/sec".format(str(self.__count_time(finish_time, start_time))))
        print("Loss: {}%".format(self.__count_loss(self.packets_sent, packets_received)))

    def __count_time(self, receive_time, send_time):
        return self.packets_sent / (receive_time - send_time).total_seconds()

    @staticmethod
    def __count_loss(packets_sent, packets_received):

        return "{0:.2f}".format((1 - (packets_received / packets_sent)) * 100)

    def close(self):
        self.__udp_socket.close()
        self.__tcp_socket.close()