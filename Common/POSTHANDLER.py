#!/usr/bin/python
import cgi

class POSTHANDLER():
    @staticmethod
    def handle(request):
        content_type = "text/plain"
        form = cgi.FieldStorage(
            fp = request.rfile,
            headers = request.headers,
            environ = { 'REQUEST_METHOD' : 'POST',
                        'CONTENT_TYPE' : request.headers['Content-Type'],
                      }) 
        # Begin the response
        request.send_response(200)
        request.send_header('Content-type', content_type)
        request.end_headers()
        message = []
        message.append('Client: %s\n' % str(request.client_address))
        message.append('User-agent: %s\n' % str(request.headers['user-agent']))
        message.append('Path: %s\n' % request.path)
        message.append('Form data:\n')
 
        # Echo back information about what was posted in the form
        for field in form.keys():
            field_item = form[field]
            if field_item.filename:
                # The field contains an uploaded file
                file_data = field_item.file.read()
                file_len = len(file_data)
                del file_data
                message.append('\tUploaded %s as "%s" (%d bytes)\n' % \
                        (field, field_item.filename, file_len))
            else:
                # Regular form value
                message.append('\t%s=%s\n' % (field, form[field].value))
         
        message = "\r\n".join(message) 
        return bytes(message, "UTF-8")
