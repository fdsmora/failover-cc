#!/usr/bin/python
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from Common.BaseServer import BaseServer

class Application(BaseServer):
    def handle_POST(self):
        print ('App: handling POST')
        print (self.form) 

    def handle_GET(self):
        action = self.get_action()
    
        response = ""
        if action == 'spit':
            response = "I AM APPLICATION"
        return response
    
    
