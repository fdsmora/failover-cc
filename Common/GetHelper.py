#!/usr/bin/python
from urllib.parse import urlparse
from Common.Utils import shell, CURL

class GetHelper(object):
    def __init__(self, request):
        self.request = request
    
    def submit_to_host(self, hostname, port, action, **values):
        url = "http://{}:{}".format(hostname, port)
        querystring = "&".join(["%s=%s" % (x[0],x[1]) for x in values.items()] )
        out, err = shell(CURL, [ "-s", url + "/" + action + "?" + querystring])
        return out, err
   
    def get_qs_values(self):
        parsed_path = urlparse(self.request.path)
        qs = parsed_path.geturl().split("?")
        if len(qs) < 2: 
            return None 
        qs = qs[1]
        value_pairs = qs.split("&")
        value_pairs = dict([ x.split("=") for x in value_pairs]) 
        return value_pairs
    '''
    @staticmethod
    def handle(request):
        status = 200
        content_type = "text/plain"
        response_content = ""
    
        parsed_path = urlparse(request.path)
        message_parts = [
                  'CLIENT VALUES:',
                  'client_address=%s (%s)' % (request.client_address,
                                              request.address_string()),
                  'command=%s' % request.command,
                  'path=%s' % request.path,
                  'real path=%s' % parsed_path.path,
                  'query=%s' % parsed_path.query,
                  'request_version=%s' % request.request_version,
                  '',
                  'SERVER VALUES:',
                  'server_version=%s' % request.server_version,
                  'sys_version=%s' % request.sys_version,
                  'protocol_version=%s' % request.protocol_version,
                  '',
                  'HEADERS RECEIVED:',
                  ]
    
        for name, value in sorted(request.headers.items()):
            message_parts.append('%s=%s' % (name, value.rstrip()))
    
        message_parts.append('')
        message = '\r\n'.join(message_parts)
    
        request.send_response(status)
        request.send_header('Content-type', content_type)
        request.end_headers()

        return bytes(message, "UTF-8")
    '''
