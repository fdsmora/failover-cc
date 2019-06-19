#!/usr/bin/python
import time
from Monitor.MonitorServer import MonitorServer, MonitorHandler
from Application.ApplicationServer import ApplicationServer, ApplicationHandler
from multiprocessing import Process
from Common.Utils import PRIMARY, STANDBY, PRIMARY_PORT, STANDBY_PORT, MONITOR_PORT

HOSTNAME = 'localhost'

def start_monitor(port, server_name, monitor=None, primary=None, standby=None):
    with MonitorServer((HOSTNAME, port), server_name, monitor, primary, standby, MonitorHandler ) as monitor_srv:
#        monitor.register_hosts(monitor=monitor, primary=primary_info, standby=standby_info)
        print(time.asctime(), monitor_srv.name + ' UP - %s:%s' % (HOSTNAME, port))
        try:    
            monitor_srv.serve_forever()
        except KeyboardInterrupt:
            pass

def start_instance(port, server_name, monitor=None, primary=None, standby=None):
    with ApplicationServer((HOSTNAME, port), server_name,  monitor, primary, standby, ApplicationHandler) as app:
#        app.register_hosts(monitor=monitor, primary=primary_info, standby=standby_info)
#        app.set_role(role)
        print(time.asctime(), app.name + ' UP - %s:%s' % (HOSTNAME, port))
        try:    
            app.serve_forever()
        except KeyboardInterrupt:
            pass

def startup():
    monitor_info= { "port" : MONITOR_PORT, "hostname" : HOSTNAME, "name":"monitor" } 
    prim1_info  = { "port" : PRIMARY_PORT, "hostname" : HOSTNAME, "name":"app1" } 
    stdby_info = { "port" : STANDBY_PORT, "hostname" : HOSTNAME, "name":"app2" } 

    monitor = Process(target=start_monitor, args=(MONITOR_PORT, "monitor"), kwargs={"primary":prim1_info, "standby":stdby_info})
    prim = Process(target=start_instance, args=(PRIMARY_PORT,"app1") , kwargs={"monitor":monitor_info, "standby":stdby_info})
    stdby = Process(target=start_instance, args=(STANDBY_PORT,"app2"), kwargs={"monitor":monitor_info, "primary":prim1_info})
    monitor.start()
    prim.start()
    stdby.start()


if __name__ == '__main__':
    startup()
