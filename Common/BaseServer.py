#!/usr/bin/python
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from abc import ABC, abstractmethod, abstractproperty
from urllib.parse import urlparse
from Common.PostHelper import PostHelper
from Common.GetHelper import GetHelper
from Common.Utils import shell, CURL


class BaseServer(HTTPServer, ABC):

  def __init__(self, hostport, name, monitor, primary, standby, handler):
    super().__init__(hostport,handler)
    self.name    = name
    self.monitor = monitor
    self.primary = primary
    self.standby = standby

  @abstractproperty
  def name(self):
      pass
 
  def GET_to_host(self, hostname, port, action, **values):
      return GetHelper.submit_to_host(self, hostname, port, action, **values)
 
  def submit_to_host(self, hostname, port, action, method, form=None, json=False):
      url = "http://{}:{}".format(hostname, port)
      out, err = ("","") 
      if method == "GET":
          out, err = shell(CURL, [ "-i", url + "/" + action])
      else:
          if json:
              out, err = shell(CURL, "-X", "POST", url + "/" + action, "-d", form , "-H", "Content-Type: application/json")
          else:
              form_str = " -F " + " -F ".join("{!s}={!r}".format(key,val) for (key,val) in form.items())
              args = [url + "/" + action]
              args.extend( form_str.split(" "))
              
          #debug
           #   print("DEBUG: FORM_STR: " + str(form_str))
              out, err = shell(CURL, args)
        
      return out, err

  '''
  def register_hosts(**hosts):
    this.monitor = hosts["monitor"]
    this.standby = hosts["standby"]
    this.primary = hosts["primary"]
  '''

  def die(self, errmsg):
      errmsg = "\n{}:ERR:{}".format(self.name, errmsg)
      print(errmsg)
      sys.exit(1)

class BaseHandler(BaseHTTPRequestHandler, ABC):
  def do_HEAD(self):
    return

  def do_GET(self):
    getHelper= GetHelper(self) 
    self.query_string = getHelper.get_qs_values()
    response = self.handle_GET()
    status = 200
    content_type = "text/plain"
    if not response:
        response = "No response from server"
    self.wfile.write(bytes(response, "UTF-8"))

  def get_action(self):
    parsed_path = urlparse(self.path)
    only_url = parsed_path.geturl().split("?")[0]
    action = only_url.split('/')[-1]
    return action
    
  def do_POST(self):
#debug
 #   print ("{}->do_POST ".format(self.server.name))
    postHelper = PostHelper(self)
    self.form=postHelper.getForm()
    response = self.handle_POST()

    status = 200
    content_type = "text/plain"
    self.send_response(status)
    self.send_header('Content-type', content_type)
    self.end_headers()
    if not response:
        response = "No response from server"
    self.wfile.write(bytes(response,"UTF-8"))
 

  @abstractmethod
  def handle_POST(self):
    pass
 
  @abstractmethod
  def handle_GET(self):
    pass
    
