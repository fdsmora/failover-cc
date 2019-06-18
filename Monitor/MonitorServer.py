#!/usr/bin/python
from Common.BaseServer import BaseServer, BaseHandler


class MonitorServer(BaseServer):
    name = "MonitorServer"
    def __init__(self, hostport, primary, standby, handler):
        super().__init__(hostport,handler)
        print("MONITOR ARGUMENTS")
        print (primary)
        print (standby)

    def register_app(self,primary, standby):
        if primary and standby:
            self.primary = primary
            self.standby = standby
           #debug
            print ("SUCCESSFULLY REGISTERED\nprim: {}:{}\nstby: {}:{}".format(primary['hostname'], primary['port'], standby['hostname'], standby['port']))
        else:
            self.die("Primary instance and standby instance must be registered together")

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

class MonitorHandler(BaseHandler):
    def handle_POST(self):
        action = self.get_action()
        if action == "update":
            out = self.server.submit_update(self.form)
            return out
    
    def handle_GET(self):
        action = self.get_action()
   
        if action == 'kill-primary':
            return self.server.kill_primary()
    
         

