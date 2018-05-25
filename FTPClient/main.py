from FTPClient.ftp import *

def print_help():
    print("Available commands:")
    print("LIST - get listing of current directory (-v option for more detailed)")
    print("CWD <dirname> - change current directory")
    print("ROOT - change current directory to root directory")
    print("RETR <filename> - download file")
    print("STOR <filename> - upload file")
    print("DEL <filename> - delete file from the server")
    print("MKD <dirname> - create new directory")
    print("HELP - get list of commands")
    print("EXIT - close connection and exit\n")


def main():
    print("Welcome to FTP CLIENT!")
    print("Enter ftp server name:")
    while True:
        server_name = input()
        # server_name = 'speedtest.tele2.net'
        log, psw = None, None
        try:
            log, psw = input("<login> <pass> (press enter if no data is needed)\n").split(" ")
        except:
            log, psw = '', ''
        ftp_conn = None
        try:
            ftp_conn = FtpConnection(server_name, log, psw)
        except:
            print("Error occured during connecting to the server!")
            print("Try again")
            continue
        print_help()
        while True:

            command = input().split(" ")
            command[0] = command[0].upper()
            if command[0] == 'RETR':
                ftp_conn.download(command[1])
            elif command[0] == 'STOR':
                ftp_conn.upload(command[1])
            elif command[0] == 'CWD':
                ftp_conn.cwd(command[1])
            elif command[0] == 'ROOT':
                ftp_conn.to_root()
            elif command[0] == 'LIST':
                try:
                    option = command[1]
                    ftp_conn.print_data(option)
                except:
                    ftp_conn.print_data()
            elif command[0] == 'DEL':
                ftp_conn.delete(command[1])
            elif command[0] == 'MKD':
                ftp_conn.make_dir(command[1])
            elif command[0] == 'HELP':
                print_help()
            elif command[0] == 'EXIT':
                ftp_conn.exit()
                exit(0)
            else:
                print("Wrong command! Type HELP to get list of commands")



if __name__ == '__main__':
    main()