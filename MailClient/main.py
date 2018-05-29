from MailClient.mail import *
import getpass

GOOGLE_PORT = 587
YANDEX_PORT = 465

def print_help():
    print("Available commands:")
    print("SEND 'msg' <recipient> - send message to recipient")
    print("SHOW <n> - show n last messages")
    print("HELP - get list of commands")
    print("EXIT - close connection and exit\n")


def main():
    print("Welcome to E-Mail CLIENT!")
    print("Enter <server_name> <server_port>")
    print("(: Google port: {} Yandex/Mail.ru port: {} :)".format(GOOGLE_PORT, YANDEX_PORT))
    while True:
        server_name, server_port = input().split(' ')

        try:
            email_conn = EmailConnection(server_name, server_port)
        except Exception as e:
            print(e)
            print("Try again")
            continue

        while True:
            log = input("Email:\n")
            psw = getpass.getpass()
            try:
                email_conn.auth(log, psw)
                break
            except smtplib.SMTPAuthenticationError as e:
                print(e)
                print("Try again")

        print_help()
        while True:
            inpt = input()
            message = inpt.split("'")
            if len(message) != 1:
                message = message[1]
            command = inpt.split(" ")
            command[0] = command[0].upper()
            if command[0] == 'SEND':
                email_conn.send_msg(message, command[-1])
            elif command[0] == 'SHOW':
                if len(command) == 1:
                    email_conn.show_messages(0)
                else:
                    email_conn.show_messages(command[1])
                try:
                    id = input()
                    email_conn.show_message(int(id))
                except KeyError:
                    pass
            elif command[0] == 'HELP':
                print_help()
            elif command[0] == 'EXIT':
                email_conn.close()
                exit(0)
            else:
                print("Wrong command! Type HELP to get list of commands")
            print("...")

if __name__ == '__main__':
    main()