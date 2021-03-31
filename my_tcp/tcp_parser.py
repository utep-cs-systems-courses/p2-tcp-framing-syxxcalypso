# Jen Sims
# CS 4375: Lab 2
#
# Collaborator: Nick Sims
import os


class TcpParser(object):
    def __init__(self, lock, files_in_use):
        self.state = self.parse
        self.final_buffer = []
        self.lock = lock
        self.files_in_use = files_in_use

    def parse(self):
        try:
            self.idx = self.temp_buffer.index(b';')
            self.tokens = self.temp_buffer[:self.idx].split(b' ')   #split spaces
            command = self.tokens[0]
            self.temp_buffer = self.temp_buffer[self.idx+1:]        #removes read msg
            self.state = eval("self."+command.decode())             #map cmd to name of funcs
            return True
        except ValueError:                                          #Index failed, need more data
            return False


    def get_size(self):
        self.size = int(self.tokens[1])                             #size of msg
        self.state = self.get_message
        return True

    def get_message(self):
        if len(self.temp_buffer) >= self.size:
            msg = self.temp_buffer[:self.size]                      #everything up to size delete(get whole msg)
            self.temp_buffer = self.temp_buffer[self.size:]         #save unread
            os.write(self.fd, msg)                                  #writes to file
            self.state = self.parse                                 #switch state
            return True
        return False

    def open(self):
        self.path = self.tokens[1].decode()                  #came in as bytes need to decode
        with self.lock:                                      #everything needs mutex
            if self.path in self.files_in_use:
                self.state = self.parse
                self.reply = b"File in use$"
                return 'Message for client'
            self.files_in_use += [self.path]                  # file open !use, mark as use, about to use
        self.fd = os.open(self.path, os.O_WRONLY | os.O_CREAT, 0o644)
        self.reply = b"All good$"
        self.state = self.parse
        return 'Message for client'

    def close(self):
        os.close(self.fd)
        with self.lock:
            self.files_in_use.remove(self.path)
        self.state = self.parse

    def fin(self):
        return "fin"

    def initiate(self):
        return self.state()
