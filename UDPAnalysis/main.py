from receiver import Receiver
from sender import Sender


def main():
    print("Welcome to UDP Analyser!")
    print("Choose whether you are sending(s) or receiving(r) packets:")
    while True:
        app_type = input()
        if app_type.lower() == "s":
            print("Enter receiver ip address:")
            ip = input()
            sender = Sender(ip)

            print("Enter 'send <n>' to send n packets to {}.".format(ip))
            print("Enter 'x' to exit.")

            while True:
                request = input().split()
                if request[0] == "send":
                    sender.send_packets(int(request[1]))
                    print("Waiting for another command...")
                elif request[0] == "x":
                    print("Closing...")
                    sender.close()
                    break
                else:
                    print("Wrong input!")
            break
        elif app_type.lower() == "r":
            receiver = Receiver()
            print("Enter 's' to start receiving packets .")
            print("Enter 'x' to exit.")

            while True:
                ipt = input()
                if ipt == "s":
                    receiver.receive_packets()
                    print("Waiting for another command...")
                elif ipt == "x":
                    receiver.close()
                    print("Closing...")
                    break
                else:
                    print("Wrong input!")
            break
        print("Wrong input!")


if __name__ == '__main__':
    main()