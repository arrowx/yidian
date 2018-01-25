#!/usr/bin/env python
# coding=utf-8

import  socket

def handle_request(client):
    buf = client.recv(1024)
    client.send("HTTP/1.1 200 OK\r\n\r\n")
    client.send('<h30>Hello web4</h10>')

def main():
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind(('0.0.0.0',80))
    sock.listen(10)
    while True:
         connection,address = sock.accept()
         handle_request(connection)
         connection.close()
if __name__ == '__main__':
    main()

