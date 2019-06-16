#!/usr/bin/python
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from Common.BaseServer import BaseServer 
from Common.Utils import shell

CURL = "/usr/bin/curl"

class Monitor(BaseServer):
    def handle_POST(self):
        print (self.form)
    
    def handle_GET(self):
        action = self.get_action()
    
        response = ""
        if action == 'communicate':
            out, err = shell(CURL, "-i", "http://localhost:8081/spit")
            response = "ACTION: %s \n OUT: %s \n ERR: %s" % (action, out, err) 
        return response
