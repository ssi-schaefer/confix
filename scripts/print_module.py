#!/usr/bin/env python

import sys
import pickle

def print_module(m):

    print '.'.join(m.name())
    print '  Priority '+`m.priority()`
    if len(m.provides()):
        print '  Provides'
        for p in m.provides():
            print '    '+`p`
    if len(m.requires()):
        print '  Requires'
        for r in m.requires():
            print '    '+`r`
    if len(m.contents()):
        print '  Contents'
        for c in m.contents():
            print '    '+`c`


for a in sys.argv[1:]:
    f = open(a, 'r')
    print_module(pickle.load(f))
    f.close()
