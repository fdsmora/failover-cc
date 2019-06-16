#!/usr/bin/python
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from Common.GETHANDLER import GETHANDLER
from Common.PostHelper import PostHelper
from abc import ABC, abstractmethod

class BaseServer(BaseHTTPRequestHandler, ABC):
  def do_HEAD(self):
    return

  def do_GET(self):
    content=GETHANDLER.handle(self)
    self.wfile.write(content)
    
  def do_POST(self):
    postHelper = PostHelper(self)
    self.form=postHelper.getForm()
#debug
#    print("FORM IS " + str(form))

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
    
  def handle_http(self):
    status = 200
    content_type = "text/plain"
    response_content = ""

    parsed_path = urlparse(self.path)
    message_parts = [
              'CLIENT VALUES:',
              'client_address=%s (%s)' % (self.client_address,
                                          self.address_string()),
              'command=%s' % self.command,
              'path=%s' % self.path,
              'real path=%s' % parsed_path.path,
              'query=%s' % parsed_path.query,
              'request_version=%s' % self.request_version,
              '',
              'SERVER VALUES:',
              'server_version=%s' % self.server_version,
              'sys_version=%s' % self.sys_version,
              'protocol_version=%s' % self.protocol_version,
              '',
              'HEADERS RECEIVED:',
              ]

    for name, value in sorted(self.headers.items()):
        message_parts.append('%s=%s' % (name, value.rstrip()))

    message_parts.append('')
    message = '\r\n'.join(message_parts)

    self.send_response(status)
    self.send_header('Content-type', content_type)
    self.end_headers()
    return bytes(message, "UTF-8")
    
