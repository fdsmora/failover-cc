#!/usr/bin/python
from Common.Utils import test_data, PRIMARY, STANDBY
from Common.BaseServer import BaseServer, BaseHandler

class ApplicationServer(BaseServer):
    name = "ApplicationServer"

    def initialize(self,role,standby=None):
        if role == PRIMARY:
            self._data = test_data
            self.standby = standby
        self.set_role(role)

    def set_role(self, role):
        self._role = role
    
    def get_role(self):
        return self._role
  
    def update(self,_map):
        if self._role != PRIMARY:
            return "Update not supported as this is not PRIMARY instance"
        for k,v in _map.items():
            if k in self._data:
                self._data[k] = v
        # Now sync the standby instance
        #out, err = self.sync_standby()
        return str(self._data)

    def sync_standby(self):
        pass

    def sync(self, json_str):
        # TODO: Convert json to dict
        pass

class ApplicationHandler(BaseHandler):
    def handle_POST(self):
    #    print ('App: handling POST')
        action = self.get_action()
        if action == "update" and self.server.get_role() == PRIMARY:
            out = self.server.update(self.form)
            return out
        if action == "sync" and self.server.get_role() == STANDBY:
            out = self.server.sync(self.form)
        
    def handle_GET(self):
        action = self.get_action()
    
        response = ""
        if action == "die":
            self.server.die("Requested to die. Farewell...")
        
        return response

