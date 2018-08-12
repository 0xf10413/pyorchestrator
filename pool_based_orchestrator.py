#!/usr/bin/env python3
# Copyright flo <flo@knightknight>
# Distributed under terms of the MIT license.
import multiprocessing as mp
import os

def f(x,y):
    from fclass import S
    S = S.get()
    print("Called with",x,y)
    try:
        return S.add(x,y)
    except RuntimeError as e:
        print("Error ! Got exception '{}' in PID {}".format(e, os.getpid()))

if __name__ == "__main__":
    with mp.Pool(5) as p:
        print(p.starmap(f, [(3,4),(1,9),(-10,5)]))

