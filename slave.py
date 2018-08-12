#!/usr/bin/env python3
# Copyright flo <flo@knightknight>
# Distributed under terms of the MIT license.

"""
Simple slave. Loads a binary python module,
answers a few questions, stop when asked.
"""
from orchestrator import Client
import socketserver as ss
import sys

class RequestHandler(ss.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("Client told us :", self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

# Simulate load from heavy C++ lib
from fclass import S
S = S.get()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("KO: Please give client name")
        sys.exit(1)
    c = Client(sys.argv[1], RequestHandler)
    print("OK: Client {} up and running".format(c.name))
    c.serve_forever()
