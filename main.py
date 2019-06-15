#!/usr/bin/env python3
import time
from http.server import HTTPServer
from server import Server

HOST_NAME = 'localhost'
PORT_NUMBER = 8080


if __name__ == '__main__':
    with HTTPServer((HOST_NAME, PORT_NUMBER), Server) as httpd:
        print(time.asctime(), 'Server UP - %s:%s' % (HOST_NAME, PORT_NUMBER))
        try:    
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
