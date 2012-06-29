#!/usr/bin/env python

from libconfix.core.machinery.repo import PackageFileRepository
from libconfix.core.utils import debug
from libconfix.core.filesys import scan

import sys
import os

for filename in sys.argv[1:]:
    if not os.path.isfile(filename):
        debug.die(filename+" is not a file")
        pass
    
    # this could certainly be done simpler :-}
    dirname = os.path.dirname(filename)
    if len(dirname) == 0:
        dirname = '.'
        pass
    filesystem = scan.scan_filesystem(dirname.split(os.sep))
    file_object = filesystem.rootdirectory().get(os.path.basename(filename))
    assert file_object is not None
    
    repo = PackageFileRepository(file_object)

    for package in repo.iter_packages():
        print 'Package: '+package.name()+' '+package.version()
        for m in package.nodes():
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
            for b in m.iter_buildinfos():
                print '      '+str(b)
                pass
            pass
        pass
    pass
