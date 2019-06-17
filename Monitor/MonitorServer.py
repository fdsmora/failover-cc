#!/usr/bin/python
from Common.BaseServer import BaseServer, BaseHandler
from Common.Utils import shell

CURL = "/usr/bin/curl"

class MonitorServer(BaseServer):
    name = "MonitorServer"
    '''    
    def __init__(self):
        super().__init__()
        self.primary = None
        self.standby = None
   '''

    def register_app(self,primary, standby):
        if primary and standby:
            self.primary = primary
            self.standby = standby
           #debug
            print ("SUCCESSFULLY REGISTERED\nprim: {}:{}\nstby: {}:{}".format(primary['hostname'], primary['port'], standby['hostname'], standby['port']))
        else:
            self.die("Primary instance and standby instance must be registered together")

class MonitorHandler(BaseHandler):
    def handle_POST(self):
        print (self.form)
    
    def handle_GET(self):
        action = self.get_action()
   
        if action == 'kill-primary':
            return self.kill_primary()

    def kill_primary(self):
        server = self.server
        primary_url = "http://{}:{}".format(server.primary["hostname"], server.primary["port"])
        out, err = shell(CURL, "-i", primary_url + "/die")
        response = "ACTION: kill-primary \n OUT: %s \n ERR: %s" % (action, out, err) 
