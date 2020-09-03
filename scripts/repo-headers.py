#!/usr/bin/env python

import sys

from libconfix.repofile import RepositoryFile
from libconfix.provide_h import Provide_CInclude

for filename in sys.argv[1:]:
    repofile = RepositoryFile(filename)
    package = repofile.load()
    for m in package.modules():
        for p in m.provides():
            if isinstance(p, Provide_CInclude):
                print str(m)+': '+str(p)
                pass
            pass
        pass
    pass
