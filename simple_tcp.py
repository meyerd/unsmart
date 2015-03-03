#!/usr/bin/python

import sys
import SocketServer

BINFILE = None

with open('samsungcom_fake.txt', 'rb') as f:
	BINFILE = f.read()

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
	data = self.request.recv(40960)
        print "{} wrote:".format(self.client_address[0])
        print repr(data)
        # just send back the same data, but upper-cased
        self.request.sendall(BINFILE)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print >>sys.stderr, "usage: %s <port>" % (sys.argv[0])
    HOST, PORT = '0.0.0.0', int(sys.argv[1])

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
