#!/usr/bin/python
import time
from Monitor.MonitorServer import MonitorServer, MonitorHandler
from Application.ApplicationServer import ApplicationServer, ApplicationHandler
from multiprocessing import Process
from Common.Utils import PRIMARY, STANDBY

HOST_NAME = 'localhost'

def start_monitor(port, primary, standby):
    with MonitorServer((HOST_NAME, port), MonitorHandler) as monitor:
        monitor.register_app(primary, standby)
        print(time.asctime(), monitor.name + ' UP - %s:%s' % (HOST_NAME, port))
        try:    
            monitor.serve_forever()
        except KeyboardInterrupt:
            pass

def start_instance(port, role, standby=None):
    with ApplicationServer((HOST_NAME, port), ApplicationHandler) as app1:
        app1.initialize(role, standby)
        print(time.asctime(), app1.name + ' UP - %s:%s' % (HOST_NAME, port))
        try:    
            app1.serve_forever()
        except KeyboardInterrupt:
            pass

def startup():
    prim1_info  = { "port" : 8081, "hostname" : "localhost" } 
    stdby1_info = { "port" : 8082, "hostname" : "localhost" } 

    monitor = Process(target=start_monitor, args=(8080,prim1_info, stdby1_info))
    app1 = Process(target=start_instance, args=(8081,PRIMARY, stdby1_info))
    stdby = Process(target=start_instance, args=(8082,STANDBY,))
    monitor.start()
    app1.start()
    stdby.start()


if __name__ == '__main__':
    startup()
