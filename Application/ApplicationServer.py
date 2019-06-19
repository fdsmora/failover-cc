#!/usr/bin/python
import json
from time import sleep
from Common.Utils import test_data, PRIMARY, STANDBY, epoch_now, HB_FRECUENCY 
from Common.BaseServer import BaseServer, BaseHandler
from threading import Thread

class ApplicationServer(BaseServer):
    name = "ApplicationServer"

    def __init__(self, *args):
        super().__init__(*args)
        self._data = test_data
        if self.standby and not self.primary:
            self.set_role(PRIMARY)
        elif self.primary and not self.standby:
            self.set_role(STANDBY)

        self.logmsg("Server up and running", self.get_role())

        self.heartbeat_run = None
        if self.get_role() == PRIMARY:
            self.start_heartbeat()

    def start_heartbeat(self):
        self.heartbeat_run = Thread(target=self.heartbeat)        
        self.heartbeat_run.start()

    def heartbeat(self):
        self.logmsg("Starting heartbeating", self.get_role(), True)
        while (True):
            monitor = self.monitor
            ts = epoch_now()
            self.logmsg("heartbeat (server_name:{}, role:{}, timestamp:{}) emitted to {}:{}".format(self.name, self.get_role(), ts, monitor["hostname"], monitor["port"] ), self.get_role(), True)
            out, err = self.GET_to_host(monitor["hostname"], monitor["port"], "heartbeat", server_name=self.name, role=self.get_role(), timestamp=ts)
            sleep(HB_FRECUENCY)

    def set_role(self, role):
        self._role = role
    
    def get_role(self):
        return self._role
  
    def update(self,_map):
#debug
 #       print ("{}->update, _map is : {}".format(self.name, _map))
        for k,v in _map.items():
            if k in self._data:
                self._data[k] = v
        # Now sync the standby instance
        if self.get_role() == PRIMARY: 
            out, err = self.sync_standby(_map)
        return str(self._data)

    def sync_standby(self, _map):
        stby_host = self.standby["hostname"]
        stby_port = self.standby["port"]
# For now, replicating the data to standby as JSON does not work, so just forward the original 'update' request to standby
#        json_data = json.dumps(self._data)
#        out, err = self.submit_to_host(stby_host, stby_port, "sync", "POST", json_data, True)  
        out, err = self.submit_to_host(stby_host, stby_port, "sync", "POST", _map)
        return out,err

    def sync(self, data):
        # as a temporary solution to the standby replication of data as JSON, just do a normal 'update' operation
        return self.update(data)

    def get_state(self):
        return str(self._data)
 
    def failover(self):
        self.switch_role()
        if self.get_role() == STANDBY:
           self.set_role(PRIMARY)
           self.logmsg("Starting as primary", self.get_role())
           self.start_heartbeat()
        else:
           self.set_role(STANDBY)
           self.logmsg("Starting as standby", self.get_role())
           # For now, heartbeat of standby is not supported, so we stop it
           if self.heartbeat_run:
               self.heartbeat_run.join()
        self.logmsg("Failover peformed, I am now a " + self.get_role())

class ApplicationHandler(BaseHandler):
    def handle_POST(self):
    #    print ('App: handling POST')
        out = ""
        action = self.get_action()
        if action == "update" and self.server.get_role() == PRIMARY:
            self.server.update(self.form)
        if action == "sync" and self.server.get_role() == STANDBY:
            out = self.server.sync(self.form)
        return out
        
    def handle_GET(self):
        action = self.get_action()
    
        response = ""
        if action == "die":
            self.server.die("Requested to die. Farewell...")
        elif action == "get-state" :
            response = self.server.get_state()
        elif action == "failover" : 
            response = self.server.failover()
        
        return response

