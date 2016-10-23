
import http.server
from datetime import datetime
import ssl
import socketserver
import pprint
import json
import re
import os
import urllib.parse
from json import JSONEncoder
import sys
import queue
import threading

PORT = int(os.environ.get('PORT', 5000))

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__   

class MQueues:
    queues = {}
    
    @staticmethod
    def hasQue(qid):
        return (qid in MQueues.queues)

    def newQue(qid):
        MQueues.queues[qid] = queue.Queue()
    
    def queEmpty(qid):
        return MQueues.hasQue(qid) and MQueues.queues[qid].empty()
    
    @staticmethod
    def get(qid):
        return MQueues.queues[qid].get()
    
    @staticmethod
    def put(qid, item):
        MQueues.queues[qid].put(item)
            
class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.responded = False
        http.server.SimpleHTTPRequestHandler.__init__(self, request, client_address, server)
        
        
    def respond(self, content):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(content) #bytes(content, 'UTF-8'))
        
        self.responded = True
    
    # respondError, etc

    def respondOk(self, code=200):
        self.send_response(code)
        self.send_header("Content-type", "application/none")
        self.end_headers()
        self.responded = True
    
    def respondEmpty(self):
        self.respondOk(204)

    def do_POST(self):
        try:
            if(self.path.startswith("/que/")):
                print("tr" , threading.current_thread())
                qid = self.path
                rSize = int(self.headers["Content-Length"])
                data = self.rfile.read(rSize)
                
                if not MQueues.hasQue(qid):
                    MQueues.newQue(qid)
                
                MQueues.queues[qid].put(data)
                self.respondOk()
            
            if not self.responded:
                # Default response
                http.server.SimpleHTTPRequestHandler.do_POST(self)
        
        except:
            print("Unexpected error:" + str(sys.exc_info()[0]))
            raise
        
    def do_GET(self):    
        try:
            if(self.path.startswith("/que/")):
                qid = self.path
                
                if MQueues.hasQue(qid):
                    if not MQueues.queEmpty(qid):
                        self.respond(MQueues.get(qid)) # MyEncoder().encode(
                    else:
                        self.respondEmpty()
            
            if not self.responded:
                # Default response
                http.server.SimpleHTTPRequestHandler.do_GET(self)
        
        except:
            print("Unexpected error:" + str(sys.exc_info()[0]))
            raise

#SocketServer.TCPServer.allow_reuse_address = True
class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
    
#httpd = ThreadingTCPServer(("localhost", PORT), Handler)
httpd = socketserver.TCPServer(("localhost", PORT), Handler)

"""
httpd = BaseHTTPServer.HTTPServer(('localhost', 4443), SimpleHTTPServer.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket (httpd.socket, certfile='path/to/localhost.pem', server_side=True)
httpd.serve_forever()
"""


print("serving at port", PORT)
httpd.serve_forever()
