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
        # allow sometime for primary to startup
        sleep(3)        
        while True:
            while retries>0:
                ts = self.primary_heartbeat["timestamp"]
                diff = epoch_now() - int(ts)
                if diff  < HB_TIMEOUT:
                    retries = HB_RETRIES
                else:
                    retries-=1
         
            self.logmsg("Failed to detect recent heartbeat from primary, performing failover...")
            # if no hearbeat detected from primary, then it's considered failed
            self.failover()

    def update_heartbeat(self, server_name, role, timestamp):
        # First check if this heartbeat is from a primary that died but came back to life, so to avoid having two primaries, let it know that it's now an standby
 #debug
        self.logmsg("update_heartbeat: my primary server name is " + self.primary["server_name"] + " and hb server_name is " + server_name + "with role " + role )
        if self.primary["server_name"] != server_name:
            self.failover_to_host(self.standby)
        with Lock() as self.hb_lock:
            self.primary_heartbeat["server_name"] = server_name
            self.primary_heartbeat["role"] = role 
            self.primary_heartbeat["timestamp"] = timestamp
            self.logmsg("heartbeat received: {}".format(self.primary_heartbeat),None,True)

    def failover(self):
        self.logmsg("starting failover")
        self.failover_on = True 
        # Wait for a little to simulate a noticable failover window
        sleep(3)
        self.failover_to_host(self.standby)
        # update host-role registry
        self.switch_role()
        # Wait a little bit more
#        sleep(2)      
        self.failover_on = False
          
    def failover_to_host(self, host):
        out, err = self.GET_to_host(host["hostname"], host["port"], "failover") 
        if not err:
            self.logmsg("Requested host {} to run failover. Done".format(host["server_name"]))
        else:
            self.logmsg("ERROR while trying to do failover on host {}:{}".format(host["server_name"], err))

class MonitorHandler(BaseHandler):
    def handle_POST(self):
        if self.server.failover_on:
            return "The system is under maintenance. Please retry later"

        action = self.get_action()
        if action == "update":
            out = self.server.submit_update(self.form)
            return out
    
    def handle_GET(self):
        action = self.get_action()

        if action != "heartbeat" and self.server.failover_on:
            return "The system is under maintenance. Please retry later"

        if action == "kill-primary":
            return self.server.kill_primary()
        elif action == "heartbeat":
            return self.server.update_heartbeat(**self.query_string)
    
         

