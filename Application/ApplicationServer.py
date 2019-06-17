#!/usr/bin/python
import json
from Common.Utils import test_data, PRIMARY, STANDBY
from Common.BaseServer import BaseServer, BaseHandler

class ApplicationServer(BaseServer):
    name = "ApplicationServer"
 
    def initialize(self,role,standby=None):
        self._data = test_data
        self.standby = standby
        self.set_role(role)
        self.name = role + ":ApplicationServer"

    def set_role(self, role):
        self._role = role
    
    def get_role(self):
        return self._role
  
    def update(self,_map):
#debug
        print ("{}->update, _map is : {}".format(self.name, _map))
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

class ApplicationHandler(BaseHandler):
    def handle_POST(self):
    #    print ('App: handling POST')
        out = ""
        action = self.get_action()
        if action == "update" and self.server.get_role() == PRIMARY:
            out = self.server.update(self.form)
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
        
        return response

