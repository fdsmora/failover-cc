#!/usr/bin/python
from Common.Utils import test_data, PRIMARY, STANDBY
from Common.BaseServer import BaseServer, BaseHandler

class ApplicationServer(BaseServer):
    name = "ApplicationServer"

    def initialize(self,role):
        if role == PRIMARY:
           self._data = test_data
           self.set_role(role)

    def set_role(self, role):
        self._role = role
    
    def get_role(self):
        return self._role
  
    def update(self,_map):
        for k,v in _map.items():
            if k in self._data:
                self._data[k] = v
        return str(self._data)

class ApplicationHandler(BaseHandler):
    def initialize(self,role):
        if role == "primary":
           self._data = test_data
           self.set_role(role)

    def handle_POST(self):
    #    print ('App: handling POST')
        action = self.get_action()
        if action == "update":
            out = self.server.update(self.form)
            return out
        
    def handle_GET(self):
        action = self.get_action()
    
        response = ""
        if action == "die":
            self.server.die("Requested to die. Farewell...")
        
        return response

    def set_role(self, role):
        self._role = role
