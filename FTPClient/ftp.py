import ftplib
import os
from FTPClient.progressbar import *

class FtpConnection:
    def __init__(self, server_name, login ='', psw = ''):
        self.ftp = ftplib.FTP(server_name)
        self.ftp.login(login, psw)
        self.root = self.ftp.pwd()

        print("Succesfully connected!")
        print("Server files:")
        self.print_data()

    def print_data(self, option=''):
        if option == '-v':
            self.ftp.retrlines('LIST')
        elif option == '':
            data = self.ftp.nlst()
            if data:
                for line in data:
                    print(line)
            else:
                print("No files in current directory!")
        else:
            print("Wrong LIST option!")

    def download(self, filename):
        try:
            filesize = self.ftp.size(filename)

            progress = AnimatedProgressBar(end=filesize, width=50)

            with open(filename, 'wb') as f:
                def callback(chunk):
                    f.write(chunk)
                    progress + len(chunk)

                    # Visual feedback of the progress!
                    progress.show_progress()

                self.ftp.retrbinary('RETR {}'.format(filename), callback)

            print("\nFile successfully downloaded!")
        except ftplib.error_perm as detail:
            print("Error: {}".format(detail))


    def upload(self,filename):
        try:
            filesize = os.path.getsize(filename)

            progress = AnimatedProgressBar(end=filesize, width=50)

            with open(filename, 'rb') as f:
                def callback(chunk):
                    progress + len(chunk)

                    # Visual feedback of the progress!
                    progress.show_progress()

                self.ftp.storbinary('STOR {}'.format(filename), f, blocksize=1024, callback=callback)

            print("\nFile successfully uploaded!")
        except (FileNotFoundError, ftplib.error_perm) as detail:
            print("Error: {}".format(detail))

    def to_root(self):
        self.cwd(self.root)


    def cwd(self, dirname):
        try:
            self.ftp.cwd(dirname)
            print("Current directory - {}".format(dirname))
        except ftplib.error_perm as detail:
            print("Error: {}".format(detail))

    def delete(self, filename):
        try:
            self.ftp.delete(filename)
            print("File successfully deleted!")
        except ftplib.error_perm as detail:
            print("Error: {}".format(detail))

    def make_dir(self, dirname):
        try:
            self.ftp.mkd(dirname)
            print("Directory successfully created!")
        except ftplib.error_perm as detail:
            print("Error: {}".format(detail))


    def exit(self):
        self.ftp.quit()