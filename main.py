#!/usr/bin/python
import time
from http.server import HTTPServer
from Monitor.monitor import Monitor 
from Application.application import Application
from multiprocessing import Process

HOST_NAME = 'localhost'

def start_monitor(port):
    with HTTPServer((HOST_NAME, port), Monitor) as monitor:
        print(time.asctime(), 'Server UP - %s:%s' % (HOST_NAME, port))
        try:    
            monitor.serve_forever()
        except KeyboardInterrupt:
            pass

def start_instance(port):
    with HTTPServer((HOST_NAME, port), Monitor) as app1:
        print(time.asctime(), 'Server UP - %s:%s' % (HOST_NAME, port))
        try:    
            app1.serve_forever()
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    monitor = Process(target=start_monitor, args=(8080,))
    app1 = Process(target=start_instance, args=(8081,))
    monitor.start()
    app1.start()

