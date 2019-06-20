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

    def kill_primary(self):
        primary_host = self.primary["hostname"]
        primary_port = self.primary["port"]
        out, err = self.submit_to_host(primary_host, primary_port, "die", "GET") 
        return "ACTION: kill-primary \n OUT: %s \n ERR: %s\n" % (out, err) 

    def submit_update(self, form):
        primary_host = self.primary["hostname"]
        primary_port = self.primary["port"]
#debug
 #       self.logmsg("UPDATING TO PRIMARY {}{} NAMED {} WITH INFO {}".format(primary_host, primary_port, self.primary["server_name"], form))
        out, err = self.submit_to_host(primary_host, primary_port, "update", "POST", form)
        return "ACTION: update \n OUT: %s \n ERR: %s\n" % (out, err) 

    def monitor_heartbeat(self):
        # allow sometime for primary to startup
        sleep(3)        
        while True:
            retries = HB_RETRIES
            while retries>0:
                ts = self.primary_heartbeat["timestamp"]

                sname = self.primary_heartbeat["server_name"]
                r = self.primary_heartbeat["role"]

                diff = epoch_now() - int(ts)
                if diff  < HB_TIMEOUT:
                 #debug
                    retries = HB_RETRIES
                else:
                    self.logmsg("EXPIRED hb FROM {},{} , RETRYING".format(sname, r))
                    retries-=1
                    sleep(2)
         
            self.logmsg("Failed to detect recent heartbeat from primary, performing failover...")
            # if no hearbeat detected from primary, then it's considered failed
            self.failover()

    def update_heartbeat(self, server_name, role, timestamp):
        # First check if this heartbeat is from a primary that died but came back to life, so to avoid having two primaries, let it know that it's now an standby
 #debug
#        self.logmsg("update_heartbeat: my primary server name is " + self.primary["server_name"] + " and hb server_name is " + server_name + "with role " + role )
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
        sleep(5)
        out, err = self.failover_to_host(self.standby)
        if not out:
            self.die("Failover failed. Nothing to do")
        # update host-role registry
        self.switch_role()
        # Wait a little bit more
#        sleep(2)      
        self.failover_on = False
          
    def failover_to_host(self, host):
        out, err = self.GET_to_host(host["hostname"], host["port"], "failover") 
        if out:
            self.logmsg("Request to host {} for failover completed".format(host["server_name"]))
        else:
            self.logmsg("ERROR while trying to do failover on host {}:{}".format(host["server_name"], err))
        return out, err

    def get_state(self, role):
        if role == "primary":
            host = self.primary
        elif role == "standby":
            host = self.standby
        out, err = self.GET_to_host(host["hostname"], host["port"], "get_state")
        return out

class MonitorHandler(BaseHandler):
    def handle_POST(self):
        if self.server.failover_on:
            return "THE SYSTEM IS UNDER MAINTENANCE. PLEASE RETRY LATER"

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
        elif action == "get_state":
            rsp = self.server.get_state(self.query_string["role"])
            return str(rsp)
    
         

