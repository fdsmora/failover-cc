#!/usr/bin/python
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from abc import ABC, abstractmethod, abstractproperty
from urllib.parse import urlparse
from Common.PostHelper import PostHelper

class BaseServer(HTTPServer, ABC):
  @abstractproperty
  def name(self):
    pass
  
  def die(self, errmsg):
      errmsg = "\n{}:ERR:{}".format(self.name, errmsg)
      print(errmsg)
      sys.exit(1)

class BaseHandler(BaseHTTPRequestHandler, ABC):
  def do_HEAD(self):
    return

  def do_GET(self):
    response = self.handle_GET()
    status = 200
    content_type = "text/plain"
    if not response:
        response = "No response from server"
    self.wfile.write(bytes(response, "UTF-8"))

  def get_action(self):
    parsed_path = urlparse(self.path)
    action = parsed_path.geturl().split('/')[-1]
    return action
    
  def do_POST(self):
    postHelper = PostHelper(self)
    self.form=postHelper.getForm()

    self.handle_POST()
    status = 200
    content_type = "text/plain"
    self.send_response(status)
    self.send_header('Content-type', content_type)
    self.end_headers()
    content = bytes(str(self.form),"UTF-8")
    self.wfile.write(content)

  @abstractmethod
  def handle_POST(self):
    pass
 
  @abstractmethod
  def handle_GET(self):
    pass
    
