#!/usr/bin/env python

# Copyright (C) 2009 Joerg Faschingbauer

# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2.1 of the
# License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

from libconfix.core.utils.error import Error
from libconfix.core.machinery.repo import AutomakePackageRepository
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const
from libconfix.core.filesys import scan
from libconfix.core.filesys.filesys import FileSystem

import optparse
import sys
import os

parser = optparse.OptionParser(version='%prog '+const.CONFIX_VERSION,
                               description='%prog [options] packages')

parser.add_option('--prefix',
                  default='/usr/local',
                  metavar='DIR',
                  help='read package information from DIR/share/confix2/repo.')

options, rest = parser.parse_args(sys.argv[1:])

if len(rest) > 1:
    raise Error('Only one package at a time can be massaged')
if len(rest) == 1:
    os.chdir(rest[0])
    pass
    
packageroot = os.getcwd().split(os.sep)

fs = scan.scan_filesystem(packageroot)
package = LocalPackage(rootdirectory=fs.rootdirectory(), setups=[])

external_nodes = []
for p in AutomakePackageRepository(prefix=options.prefix.split(os.sep)).iter_packages():
    if p.name() != package.name():
        external_nodes.extend(p.nodes())
        pass
    pass

package.boil(external_nodes=external_nodes)
package.output()
fs.sync()
