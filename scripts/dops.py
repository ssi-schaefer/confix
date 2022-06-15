#!/usr/bin/env python

from libconfix.repofile import RepositoryFile
from libconfix.provide_h import Provide_CInclude
import sys

all_my_headers = set()

for filename in sys.argv[1:]:
    repofile = RepositoryFile(filename)
    package = repofile.load()
    for m in package.modules():
        for p in m.provides():
            if isinstance(p, Provide_CInclude):
                all_my_headers.add(p.string())
                pass
            pass
        pass
    pass
    
for headerfile in all_my_headers:
    print(headerfile)
    pass

