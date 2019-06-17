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

    def submit_to_primary(self, action, method, form=None):
        primary_url = "http://{}:{}".format(self.primary["hostname"], self.primary["port"])
        out, err = ("","") 
        if method == "GET":
            out, err = shell(CURL, "-i", primary_url + "/" + action)
        else:
            form_str = " -F ".join("{!s}={!r}".format(key,val) for (key,val) in form.items())
            #debug
            print("DEBUG: FORM_STR: " + form_str)
            out, err = shell(CURL, primary_url + "/" + action, "-F", form_str)
        
        return out, err

    def kill_primary(self):
        out, err = self.submit_to_primary("die", "GET") 
        return "ACTION: kill-primary \n OUT: %s \n ERR: %s\n" % (out, err) 

    def submit_update(self, form):
        out, err = self.submit_to_primary("update", "POST", form)
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
    
         

