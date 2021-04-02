# Jen Sims
# CS 4375: Lab 2
#
# Collaborator: Nick Sims
#
# State machine to implement protocol, server handles communication with client, passing
# message into the parser.
import os


class TcpParser(object):
    def __init__(self, lock, files_in_use):
        self.state = self.parse                                     #start state (default)
        self.lock = lock                                            #mutex
        self.files_in_use = files_in_use                            #if file open (!override)

    # open file.txt;size 5;helloclose
    def parse(self):
        try:
            self.idx = self.temp_buffer.index(b';')                 #finds ;
            self.tokens = self.temp_buffer[:self.idx].split(b' ')   #split spaces
            command = self.tokens[0]
            self.temp_buffer = self.temp_buffer[self.idx+1:]        #removes read msg
            self.state = eval("self."+command.decode())             #map cmd to name of funcs; prep trans
            return True                                             #worked
        except ValueError:                                          #Index failed, need more data
            return False                                            #!work


    def get_size(self):
        self.size = int(self.tokens[1])                             #size of msg
        self.state = self.get_message                               #prep transition
        return True

    def get_message(self):
        if len(self.temp_buffer) >= self.size:
            msg = self.temp_buffer[:self.size]                      #everything up to size delete(get whole msg)
            self.temp_buffer = self.temp_buffer[self.size:]         #save unread
            os.write(self.fd, msg)                                  #writes data sent 4rm client
            self.state = self.parse                                 #switch state
            return True
        return False

    def open(self):
        self.path = self.tokens[1].decode()                  #came in as bytes need to decode
        with self.lock:                                      #everything needs mutex
            if self.path in self.files_in_use:
                self.state = self.parse
                self.reply = b"File in use$"                #send to client
                return 'Message for client'                 #telling server to send reply
            self.files_in_use += [self.path]                  # file open !use, mark as use, about to use
        self.fd = os.open(self.path, os.O_WRONLY | os.O_CREAT, 0o644) #opens file, returns fd to be used by os.write
        self.reply = b"All good$"                               #tell server, send msg to client start sending msg
        self.state = self.parse
        return 'Message for client'                             #telling server, send reply (All good)

    def close(self):                                            #client tell server, done, write evtyhin
        os.close(self.fd)
        with self.lock:
            self.files_in_use.remove(self.path)                 #release file from use
        self.state = self.parse

    def fin(self):                                              #return end msg to server
        return "fin"

    def initiate(self):                                         #.call() state machine
        return self.state()
