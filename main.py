#!/usr/bin/python
import time
from Monitor.MonitorServer import MonitorServer, MonitorHandler
from Application.ApplicationServer import ApplicationServer, ApplicationHandler
from multiprocessing import Process
from Common.Utils import PRIMARY, STANDBY

HOSTNAME = 'localhost'

def start_monitor(port, primary, standby):
    with MonitorServer((HOSTNAME, port), primary, standby, MonitorHandler ) as monitor:
#        monitor.register_hosts(monitor=monitor, primary=primary_info, standby=standby_info)
        print(time.asctime(), monitor.name + ' UP - %s:%s' % (HOSTNAME, port))
        try:    
            monitor.serve_forever()
        except KeyboardInterrupt:
            pass

def start_instance(port, monitor, primary=None, standby=None):
    with ApplicationServer((HOSTNAME, port),  monitor, primary, standby, ApplicationHandler) as app:
#        app.register_hosts(monitor=monitor, primary=primary_info, standby=standby_info)
#        app.set_role(role)
        print(time.asctime(), app.name + ' UP - %s:%s' % (HOSTNAME, port))
        try:    
            app.serve_forever()
        except KeyboardInterrupt:
            pass

def startup():
    primary_port = 8084
    standby_port = 8087
    monitor_port = 8080 
    monitor_info= { "port" : monitor_port, "hostname" : HOSTNAME, "name":"monitor" } 
    prim1_info  = { "port" : primary_port, "hostname" : HOSTNAME, "name":"app1" } 
    stdby_info = { "port" : standby_port, "hostname" : HOSTNAME, "name":"app2" } 

    monitor = Process(target=start_monitor, args=(monitor_port,), kwargs={"primary":prim1_info, "standby":stdby_info})
    prim = Process(target=start_instance, args=(primary_port,) , kwargs={"monitor":monitor_info, "standby":stdby_info})
    stdby = Process(target=start_instance, args=(standby_port,), kwargs={"monitor":monitor_info, "primary":prim1_info})
    monitor.start()
    prim.start()
    stdby.start()


if __name__ == '__main__':
    startup()
