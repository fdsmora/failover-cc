#!/usr/bin/python
import time
from Monitor.MonitorServer import MonitorServer, MonitorHandler
from Application.ApplicationServer import ApplicationServer, ApplicationHandler
from multiprocessing import Process
from Common.Utils import PRIMARY, STANDBY

HOST_NAME = 'localhost'

def start_monitor(port, primary, standby):
    with MonitorServer((HOST_NAME, port), MonitorHandler) as monitor:
        print(time.asctime(), 'Monitor server UP - %s:%s' % (HOST_NAME, port))
        monitor.register_app(primary, standby)
        try:    
            monitor.serve_forever()
        except KeyboardInterrupt:
            pass

def start_instance(port):
    with ApplicationServer((HOST_NAME, port), ApplicationHandler) as app1:
        print(time.asctime(), 'Application server UP - %s:%s' % (HOST_NAME, port))
        app1.initialize(PRIMARY)
        try:    
            app1.serve_forever()
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    prim1_info  = { "port" : 8081, "hostname" : "localhost" } 
    stdby1_info = { "port" : 8082, "hostname" : "localhost" } 

    monitor = Process(target=start_monitor, args=(8080,prim1_info, stdby1_info))
    app1 = Process(target=start_instance, args=(8081,))
    monitor.start()
    app1.start()

