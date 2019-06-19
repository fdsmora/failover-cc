#!/usr/bin/python
from Common.BaseServer import BaseServer, BaseHandler
from Common.Utils import epoch_now, HB_TIMEOUT, HB_RETRIES 
from threading import Lock, Thread
from time import sleep

class MonitorServer(BaseServer):
    name = "MonitorServer"

    def __init__(self, *args):
        super().__init__(*args)
        # heartbeating monitoring
        self.primary_heartbeat = { "server_name" : "", "role" : "", "timestamp" : 0 }
        self.hb_lock = None
        # flag to indicate whether failover is going on
        self.failover_on = False 
        hb_monitoring = Thread(target=self.monitor_heartbeat)
        hb_monitoring.start()
                

    '''
    def register_app(self,primary, standby):
        if primary and standby:
            self.primary = primary
            self.standby = standby
           #debug
            print ("SUCCESSFULLY REGISTERED\nprim: {}:{}\nstby: {}:{}".format(primary['hostname'], primary['port'], standby['hostname'], standby['port']))
        else:
            self.die("Primary instance and standby instance must be registered together")
    '''

    def kill_primary(self):
        primary_host = self.primary["hostname"]
        primary_port = self.primary["port"]
        out, err = self.submit_to_host(primary_host, primary_port, "die", "GET") 
        return "ACTION: kill-primary \n OUT: %s \n ERR: %s\n" % (out, err) 

    def submit_update(self, form):
        primary_host = self.primary["hostname"]
        primary_port = self.primary["port"]
        out, err = self.submit_to_host(primary_host, primary_port, "update", "POST", form)
        return "ACTION: update \n OUT: %s \n ERR: %s\n" % (out, err) 

    def monitor_heartbeat(self):
        retries = HB_RETRIES
        # allow sometime for primary to go up
        sleep(3)        
        print ("ENTERED MONITOR HEARTBEAT")
        while retries>0:
            ts = self.primary_heartbeat["timestamp"]
            diff = epoch_now() - int(ts)
            if diff  < HB_TIMEOUT:
                retries = HB_RETRIES
         #       self.logmsg("HEARTBEAT FINE, diff is : " + str(diff))
            else:
                retries-=1
         
        print ("HEARTBEAT FAILED")
        # if no hearbeat detected from primary, then it's considered failed
          # sleep many seconds to simulate a noticable failover
#        self.failover()

    def update_heartbeat(self, server_name, role, timestamp):
        with Lock() as self.hb_lock:
            self.primary_heartbeat["server_name"] = server_name
            self.primary_heartbeat["role"] = role 
            self.primary_heartbeat["timestamp"] = timestamp
            print ("{}, heartbeat received: {}".format(self.name, self.primary_heartbeat))

#    def failover(self):
         

class MonitorHandler(BaseHandler):
    def handle_POST(self):
        action = self.get_action()
        if action == "update":
            out = self.server.submit_update(self.form)
            return out
    
    def handle_GET(self):
        action = self.get_action()
   
        if action == "kill-primary":
            return self.server.kill_primary()
        elif action == "hearbeat":
            return self.server.update_heartbeat(**self.query_string)
    
         

