#!/usr/bin/env python3
import os, socket, sys, re

server_host = '127.0.0.1'
server_port = int(sys.argv[1])

def main():

    if not (sock := open_socket(server_host, server_port)):
        return

    msg = f'open {sys.argv[3]};'.encode()                            #msg framing
    while len(msg):                                                  #send len(msg)
        sent = sock.send(msg)
        msg = msg[sent:]

    reply = b''
    while not b'$' in (reply := reply + sock.recv(1024)):         #!terminate, keep asking 4 data
        pass

    if reply != b'All good$':
        os.write(2, 'File in use')
        return

    f = os.open(sys.argv[2], os.O_RDONLY)
    while (data := os.read(f, 1024)) != b'':                        #read data in mem
        send(data, sock)                                            #continously send data
    os.close(f)

    end = b'close;'                                                  #closes file @ server
    while len(end):
        sent = sock.send(end)
        end = end[sent:]

    sock.shutdown(socket.SHUT_WR)
    sock.close()


def open_socket(server_host, server_port):
    sock = None
    for addr_info in socket.getaddrinfo(server_host, server_port, socket.AF_UNSPEC, socket.SOCK_STREAM):
        addr_family, sock_type, proto, canonical_name, sock_addr = addr_info
        try:
            sock = socket.socket(addr_family, sock_type, proto)
        except socket.error as err:
            sock = None
            continue

        try:
            sock.connect(sock_addr)
        except socket.error as err:
            sock.close()
            sock = None
            continue
    return sock


def send(msg, sock):
    init_frame = f'get_size {len(msg)};'.encode()
    data = init_frame + msg

    while len(data):
        sent = sock.send(data)
        data = data[sent:]

if __name__ == '__main__':
    main()
