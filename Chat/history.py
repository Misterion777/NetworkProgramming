from datetime import datetime
import re

DATE_FORMAT = '%m/%d/%Y'
HISTORY = 'history.txt'
ALL = "All"

class History:
    def __init__(self):    
        self.current_date = datetime.today().strftime(DATE_FORMAT)   
        try:
            f = open(HISTORY, "r+")   
            dateinfo = f.readline().rstrip('\n')    
            if not self.is_up_to_date(dateinfo):
                f.close()
                f = open(HISTORY, "w")   
                f.writelines([self.current_date,'\n'])     
        except FileNotFoundError:
            f = open(HISTORY, "w+")  
            f.writelines([self.current_date,'\n'])   
            
        f.close()       

    def is_up_to_date(self, prev_date):
        return self.current_date == prev_date

    def write_to_file(self, sender, receiver, message):
        header_format = '{} - {}:'.format(sender, receiver)
        current_time = datetime.strftime(datetime.now(), "%H:%M: ")

        sender_met = False
        f = open(HISTORY, 'r')
        content = f.readlines()
        f.close()
        new_content = []   
        ending = []    
        for i in range(len(content)):
            if sender_met:
                if content[i] =='\n':
                    ending = content[i:]
                    new_content = content[:i]
                    new_content.extend([current_time + message,'\n'])
                    break
            if self.valid_header(content[i], sender):
                sender_met = True

        if not sender_met:
            f = open(HISTORY, 'a')
            f.writelines(['\n', header_format +'\n', current_time + message, '\n', '\n'])
        else:
            f = open(HISTORY, 'w')
            ending.append('\n')
            f.writelines(new_content + ending)
        f.close()

    def read_from_file(self, sender):
        sender_met = False
        f = open(HISTORY, 'r')
        content = f.readlines()
        f.close()
        stin = ""
        message_list = []
        start_index = 0
        for i in range(len(content)):
            if sender_met:
                if content[i] == '\n':
                    message_list.extend(content[start_index:i])
                    sender_met = False
            if self.valid_header(content[i], sender) or content[i].__contains__(ALL):
                sender_met = True
                start_index = i
        return [line.rstrip('\n') for line in message_list]


    def valid_header(self, header, sender):
        if re.search('\w* - \w*', header):
            if header.__contains__(sender):
                return True
        return False
