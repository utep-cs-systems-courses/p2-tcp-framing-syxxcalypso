# Jen Sims
# CS 4375: Lab 2
#
# Collaborator: Nick Sims

class TcpParser(object):
    def __init__(self):
        self.state = self.parse
        self.final_buffer = []

    def parse(self):
        try:
            self.idx = self.temp_buffer.index(';')
            self.tokens = self.temp_buffer[:self.idx].split(' ')
            command = self.tokens[0]
            self.state = eval("self."+command)
            return True
        except ValueError:                                          # Index failed, need more data
            return False


    def size(self):
        self.size = int(self.tokens[1])
        self.idz = self.size + self.idx + 1
        self.state = self.get_message
        return True

    def get_message(self):
        if len(self.temp_buffer[self.idx+1:]) >= self.size:
            msg = self.temp_buffer[self.idx+1:self.idz]
            self.temp_buffer = self.temp_buffer[self.idz:]
            self.final_buffer += [msg]
            self.state = self.parse
            return True
        return False

    def fin(self):
        return "fin"

    def initiate(self):
        return self.state()
