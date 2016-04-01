from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urllib
import sys
import os

class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        path = directory+"/"+removeIllegal(self.path)
        if os.path.isfile(path):
            tempFile = open(path,"rb")
            content = tempFile.read()
            tempFile.close()
        else:
            try:
                content = urllib.urlopen(url+self.path).read()
                urllib.urlretrieve(url+self.path,path)
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

def getServer(port):
    BaseHTTPRequestHandler.server_version = "Microsoft-IIS/8.0"
    BaseHTTPRequestHandler.sys_version = ""
    return HTTPServer(("",port), myHandler)

def verify(url,directory):
    if not os.path.exists(directory):
        try:
            urllib.urlopen(url)
            os.makedirs(directory)
        except:
            sys.exit()

def removeIllegal(path):
    for item in '\/:*?"<>|':
        path = path.replace(item,"_")
    return path

if __name__ == "__main__":
    url = raw_input("URL: ")
    port = int(raw_input("Port: "))
    directory = removeIllegal(url)
    verify(url,directory)
    server = getServer(port)
    print "Replicating {} on port {}".format(url,port)
    server.serve_forever()


