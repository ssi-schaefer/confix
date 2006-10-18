#!/usr/bin/env python

import sys

from libconfix.repofile import RepositoryFile

for filename in sys.argv[1:]:
    repofile = RepositoryFile(filename)
    package = repofile.load()
    print 'Package: '+package.name()+' '+package.version()
    for m in package.modules():
        print '  Module: '+str(m)
        print '    Provides: '
        for p in m.provides():
            print '      '+str(p)
            pass
        print '    Requires: '
        for r in m.requires():
            print '      '+str(r)
            pass
        print '    Buildinfos: '
        for b in m.buildinfos():
            print '      '+str(b)
            pass
        pass
    pass
