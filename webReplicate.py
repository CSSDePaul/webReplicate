from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urllib
import sys
import os

URL = raw_input("URL: ")
PORT = int(raw_input("Port: "))
illegal = '\/:*?"<>|'

def removeIllegal(path):
    for item in illegal:
        path = path.replace(item,"_")
    return path

dirURL = removeIllegal(URL)
if not os.path.exists(dirURL):
    try:
        urllib.urlopen(URL)
        os.makedirs(dirURL)
    except:
        sys.exit()

class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        path = dirURL+"/"+removeIllegal(self.path)
        if os.path.isfile(path):
            tempFile = open(path,"rb")
            content = tempFile.read()
            tempFile.close()
        else:
            try:
                content = urllib.urlopen(URL+self.path).read()
                urllib.urlretrieve(URL+self.path,path)
            except:
                content =   '''
                            <html>
                            <head>
                            <title>
                            404 Error
                            </title>
                            </head>
                            <body>
                            <center>
                            <h1>404 Not Found</h1>
                            </center>
                            </body>
                            </html>
                            '''
        self.wfile.write(content)
        return

try:
    BaseHTTPRequestHandler.server_version = "Microsoft-IIS/8.0"
    BaseHTTPRequestHandler.sys_version = ""
    server = HTTPServer(("",PORT), myHandler)
    print "Replicating {} on port {}".format(URL,PORT)
    server.serve_forever()
except KeyboardInterrupt:
    server.socket.close()


