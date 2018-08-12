#!/usr/bin/env python3
# Copyright flo <flo@knightknight>
# Distributed under terms of the MIT license.
import subprocess
import socketserver as ss
import socket as s
import os
import time
import sys

"""
Orchestrator in python. Launches processes, keep contact with them
using pipes.
"""

# TODO: use unix sockets
# TODO: use unbuffered mode (PYTHONUNBUFFERED)


class Client(object):

    def __init__(self, name, request_handler_class):
        self.name = name
        self.sock_name = "./{}.sock".format(name)
        self._try_to_clean_sock(self.sock_name)
        self.server = ss.UnixStreamServer(self.sock_name, request_handler_class)

    def _try_to_clean_sock(self, sock_name):
        try:
            os.unlink(sock_name)
        except OSError:
            if os.path.exists(sock_name):
                raise

    def serve_forever(self):
        self.server.serve_forever()

N = 5

if __name__ == "__main__":
    proc = subprocess.Popen(["python", "-u", "slave.py", "aaa"], stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
    first_msg = proc.stdout.readline()
    print("Client said", first_msg)
    if first_msg.startswith(b"KO"):
        print("Client KO, stopping")
        sys.exit(1)
    sock = s.socket(s.AF_UNIX, s.SOCK_STREAM)
    sock.connect("./aaa.sock")
    print("Sending 'abc'")
    sock.sendall(b'abc')
    print("Received", sock.recv(16))
    proc.send_signal(2)
