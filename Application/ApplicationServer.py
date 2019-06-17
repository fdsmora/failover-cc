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

class ApplicationHandler(BaseHandler):
    def initialize(self,role):
        if role == "primary":
           self._data = test_data
           self.set_role(role)

    def handle_POST(self):
        print ('App: handling POST')
        print (self.form) 

    def handle_GET(self):
        action = self.get_action()
    
        response = ""
        if action == 'spit':
            response = "I AM APPLICATION"
        return response

    def set_role(self, role):
        self._role = role
