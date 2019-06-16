#!/usr/bin/python
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from Common.Utils import test_data 
from Common.BaseHandler import BaseHandler

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
