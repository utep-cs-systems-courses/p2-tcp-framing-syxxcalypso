#!/usr/bin/env python3
import os
import socket, sys, re
from tcp_parser import TcpParser                                        # import Class
from threading import Thread, Lock

def main():
    try:
        lock = Lock()
        files_in_use = []

        source_addr = ''
        source_port = int(sys.argv[1])
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((source_addr, source_port))
        sock.listen(1)

        while True:
            conn, addr = sock.accept()
            Thread(target=run, args=(conn, addr, files_in_use, lock)).start()   #Start new thread, run run()
                                                                            #mul threads for mul clients
    except KeyboardInterrupt:
        conn.close()

def run(conn, addr, files_in_use, lock):                           #runs threads. each thread calls run()
    os.write(2, f'[==] (ACCEPT) :: ADDR<{addr}>'.encode())

    my_parser = TcpParser(lock, files_in_use)                                 #instantiate TcpParser
    my_parser.temp_buffer = conn.recv(4)                                    #recv 4 bytes, ->TcpParser

    while True:                                                     #infinite loop to run

        result = my_parser.initiate()                           #.call() state machine

        if result == 'fin':                                     #done
            break

        elif result == 'Message for client':
            message = my_parser.reply                           #msg about to get sent to client
            while len(message):
                sent = conn.send(message)                       #send rtrns # of bytes
                message = message[sent:]                        #cuts bytes already sent


        elif result == False:
            my_parser.temp_buffer += conn.recv(4)



    conn.shutdown(socket.SHUT_WR)
    conn.close()

if __name__ == '__main__':
    main()
