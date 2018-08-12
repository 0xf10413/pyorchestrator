#!/usr/bin/env python3
# Copyright flo <flo@knightknight>
# Distributed under terms of the MIT license.
import multiprocessing as mp
import os
import time
import sys
from select import select

"""
Orchestrator in python. Launches processes, keep contact with them
using pipes.
"""

# TODO: a clean class for a child and communication
# TODO: a protocol (status code + status message + reply message ?)

def entry_point(conn):
    """
    Entry point for a producer.
    :param conn Connection of a full-duplex pipe. The other end is expected to be owned by
    the orchestrator itself
    """
    # custom imports, if you need c/c++ code
    #from fclass import S
    pid = os.getpid()
    print("Child {}: Up and running! Waiting for orders…".format(pid))
    conn.send("OK: finished startup")
    alive = True
    while alive:
        if conn.poll():
            data_sent = conn.recv()
            reply = ""
            print("Child {}: got some data ! Parent said…".format(pid), data_sent)
            if isinstance(data_sent, str):
                if data_sent == "stop":
                    print("Child {}: got shutdown message, stopping…".format(pid))
                    reply = "OK: shutdown complete"
                    alive = False
                elif data_sent.startswith("add"):
                    add, x, y = data_sent.split()
                    print("Child {}: add message, adding {} and {}".format(pid, x, y))
                    x, y = int(x), int(y)
                    reply = "OK: {} + {} is {}".format(x, y, x + y)
                    time.sleep(x+y/3) # arbitrary slowdown
            else:
                print("Child {}: unknown operation '{}', ignoring".format(pid, data_sent))
                reply = "Warning"
            conn.send(reply)
        else:
            print("Child {} : no order received, sleeping for 1s…".format(pid))
            time.sleep(1)
    print("Child {}: shutdown finished".format(pid))


if __name__ == "__main__":
    # Prepare multiple childs
    proc_conns = []
    child_conns = [] # to ensure child connection does not die too soon and get an EOFerror
    nb_proc = 5
    for i in range(nb_proc):
        child_conn, parent_conn = mp.Pipe()
        proc = mp.Process(target=entry_point, args=(child_conn,))
        proc.start()
        # waiting for the init message
        print("Parent: child said", parent_conn.recv())
        proc_conns.append((proc, parent_conn))
        child_conns.append(child_conn)

    # Send messages to some of them
    messages = ["add 3 2", "add 1 5", "add 6 7"]
    for msg, (proc, conn) in zip(messages, proc_conns):
        print("Parent: now sending '{}' to the child {}".format(msg, proc.pid))
        conn.send(msg)

    # Asynchronous receive
    nb_msg_received = 0
    while nb_msg_received < len(messages):
        rlist, wlist, xlist = select([conn for proc, conn in proc_conns], [], [], 0)
        if not rlist:
            print("Parent: no child answer (got {}/{}), sleeping for 1s…".
                    format(nb_msg_received, len(messages)))
            time.sleep(1)
            continue
        for conn in rlist:
            print("Parent: got message {} !".format(conn.recv()))
            nb_msg_received += 1

    # Send stop message to some of them
    for proc, conn in proc_conns:
        print("Parent: now stopping child {}".format(proc.pid))
        conn.send("stop")

    # Asynchronous receive stop
    nb_msg_received = 0
    while nb_msg_received < nb_proc:
        rlist, wlist, xlist = select([conn for proc, conn in proc_conns], [], [], 0)
        if not rlist:
            print("Parent: no child answer (got {}/{}), sleeping for 1s…".
                    format(nb_msg_received, nb_proc))
            time.sleep(1)
            continue
        for conn in rlist:
            print("Parent: got message {} !".format(conn.recv()))
            nb_msg_received += 1

    # Final join
    for proc, _ in proc_conns:
        proc.join()

