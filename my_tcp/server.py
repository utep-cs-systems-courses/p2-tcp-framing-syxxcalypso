#!/usr/bin/env python3
import socket, sys, re
from tcp_parser import TcpParser                                        # import Class


def run():
    try:
        source_addr = ''
        source_port = int(sys.argv[1])
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((source_addr, source_port))
        sock.listen(1)

        conn, addr = sock.accept()
        print(f'[==] (ACCEPT) :: ADDR<{addr}>')

        my_parser = TcpParser()                                         #instantiate TcpParser
        my_parser.temp_buffer = conn.recv(4).decode()                   #recv 4 bytes, ->TcpParser

        while True:                                                     #infinite loop to run

            result = my_parser.initiate()

            if result == 'fin':
                break

            elif result == False:
                my_parser.temp_buffer += conn.recv(4).decode()

        print("Out of Infinite Loop")

        while len(msg):
            sent = conn.send(msg.encode())
            msg = msg[sent:]

    except KeyboardInterrupt:
        conn.close()

    conn.shutdown(socket.SHUT_WR)
    conn.close()

if __name__ == '__main__':
    run()
