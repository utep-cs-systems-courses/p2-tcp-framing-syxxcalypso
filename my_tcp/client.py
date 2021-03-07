#!/usr/bin/env python3
import socket, sys, re

server_host = '127.0.0.1'
server_port = int(sys.argv[1])

def run():

    if not (sock := open_socket(server_host, server_port)):
        print('[EE] (CONNECT) :: [FATAL] Cannot establish socket connection')
        return

    msg = sys.argv[2]
    print(f'DATUM: {msg}')
    send(msg, sock)


def open_socket(server_host, server_port):
    sock = None
    for addr_info in socket.getaddrinfo(server_host, server_port, socket.AF_UNSPEC, socket.SOCK_STREAM):
        addr_family, sock_type, proto, canonical_name, sock_addr = addr_info
        try:
            sock = socket.socket(addr_family, sock_type, proto)
            print(f'[==] (CREATE SOCKET) :: AF<{addr_family}> TYPE<{sock_type}> PROTOCOL<{proto}>')
        except socket.error as err:
            print('[EE] (CREATE SOCKET) :: err')
            sock = None
            continue

        try:
            sock.connect(sock_addr)
            print(f'[==] (CONNECT) :: TARGET<{sock_addr}>')
        except socket.error as err:
            print(f'[EE] (CONNECT) :: {err}')
            sock.close()
            sock = None
            continue
    return sock


def send(msg, sock):
    init_frame = f'size {len(msg)};'
    end_frame = 'fin;'
    data = init_frame + msg + end_frame

    while len(data):
        sent = sock.send(data.encode())
        print(f'[==] (SEND) :: MSG<{data[:sent]}>')
        data = data[sent:]

    reply = sock.recv(1024).decode()
    print(f'[==] (RECEIVE) :: MSG<{reply}>')

    while 1:
        reply = sock.recv(1024).decode()
        print("Received '%s'" % reply)
        if len(reply) == 0:
            break
    print(f'[==] (REPLY EMPTY) :: Closing')

    sock.shutdown(socket.SHUT_WR)
    sock.close()

if __name__ == '__main__':
    run()
