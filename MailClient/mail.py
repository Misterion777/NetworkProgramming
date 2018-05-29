import smtplib
import imaplib
import email.utils
from email.mime import text

class ImapConnection():
    def __init__(self, servername):
        self.servername = servername
        self.__proccess_servername()
        self.emails = {}

    def __proccess_servername(self):
        imap = 'imap.'
        if not self.servername.startswith(imap):
            self.servername = imap + self.servername


    def read_emails(self, n, login, password):
        n = int(n)

        self.emails.clear()
        mail = None
        try:
            mail = imaplib.IMAP4_SSL(self.servername)
            mail.login(login, password)
            mail.select('inbox')

            type, data = mail.search(None, 'ALL')
            mail_ids = data[0]

            id_list = mail_ids.split()
            first_email_id = int(id_list[0])
            latest_email_id = int(id_list[-1])

            if n == 0:
                n = latest_email_id

            for i in range(latest_email_id, first_email_id, -1):
                if latest_email_id - i >= int(n):
                    break
                type, new_data = mail.fetch(str(i), '(RFC822)')
                msg = email.message_from_bytes(new_data[0][1])
                email_subject = msg['subject']
                email_from = msg['from']
                print("Message ID: {}".format(i))
                print('From : ' + email_from)
                self.emails[i] = msg
        except Exception as e:
            print(e)
        mail.close()
        print("Messages succesfully shown!")
        print("If you'd like to see any content, type in message id, otherwise press enter.")


    def show_body(self, id):
        if self.emails[id].is_multipart():
            for payload in self.emails[id].get_payload():
                print(payload.get_payload())
        else:
            print(self.emails[id].get_payload())

class SmtpConnection():
    def __init__(self, servername, port):
        self.username = ""
        self.port = port
        self.servername = servername
        self.__proccess_servername()

        self.server = smtplib.SMTP(self.servername, port)
        self.server.connect(self.servername, port)
        # self.server.set_debuglevel(True)

        print("Successfully connected!")

    def login(self, username, password):
        self.username = username
        self.__check_for_tls()
        self.server.login(username, password)


    def __proccess_servername(self):
        smtp = 'smtp.'
        if not self.servername.startswith(smtp):
            self.servername = smtp + self.servername

    def __form_message(self, body, recipient_email):
        msg = text.MIMEText(body)
        msg['To'] = email.utils.formataddr(('Recipient', recipient_email))
        msg['From'] = email.utils.formataddr(('Author', self.username))
        msg['Subject'] = 'Sent by PyEmailClient'
        return msg

    def __check_for_tls(self):
        self.server.ehlo()

        if self.server.has_extn('STARTTLS'):
            self.server.starttls()
            self.server.ehlo()

    def send_message(self, body, recipient_email, password):
        self.server.connect(self.servername, self.port)
        self.login(self.username, password)
        msg = self.__form_message(body, recipient_email)
        self.server.sendmail(self.username, [recipient_email], msg.as_string())
        self.close()

    def close(self):
        self.server.quit()


class EmailConnection():
    def __init__(self, servername, smtp_port):
        self.username = ''
        self.password = ''
        self.smtp_connection = SmtpConnection(servername, smtp_port)
        self.imap_connection = ImapConnection(servername)


    def auth(self, username, password):
        self.username = username
        self.password = password
        self.smtp_connection.login(username, password)
        print("Successfully authenticated!")
        self.smtp_connection.close()

    def send_msg(self, msg, recipient):
        self.smtp_connection.send_message(msg,recipient, self.password)
        print("Successfully sent!")


    def show_messages(self, n):
        self.imap_connection.read_emails(n, self.username, self.password)

    def show_message(self, id):
        self.imap_connection.show_body(id)


    def close(self):
        self.smtp_connection.close()
