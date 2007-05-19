# Copyright (C) 2006-2007 Joerg Faschingbauer

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

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.utils import const
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.automake import bootstrap, configure, make
from libconfix.testutils.persistent import PersistentTestCase

from libconfix.plugins.c.setups.default_setup import DefaultCSetup
from libconfix.plugins.c.executable import ExecutableBuilder

import unittest
import sys
import os

class ExecutableNameBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(ExplicitExecutableNameBuildTest('test'))
        pass
    pass

class ExplicitExecutableNameBuildTest(PersistentTestCase):
    def test(self):
        fs = FileSystem(path=self.rootpath())
        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())
        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())
        install=fs.rootdirectory().add(
            name='install',
            entry=Directory())

        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("'+self.__class__.__name__+'")',
                              'PACKAGE_VERSION("1.2.3")']))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File())
        source.add(
            name='main.cc',
            entry=File(lines=['// CONFIX:EXENAME("explicit-name")',
                              'int main() { return 0; }']))

        package = LocalPackage(rootdirectory=source,
                               setups=[DefaultCSetup(short_libnames=False, use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        fs.sync()

        bootstrap.bootstrap(
            packageroot=source.abspath(),
            path=None,
            use_libtool=False,
            use_kde_hack=False,
            argv0=sys.argv[0])
        configure.configure(
            packageroot=source.abspath(),
            builddir=build.abspath(),
            prefix=install.abspath(),
            readonly_prefixes=None)
        make.make(
            builddir=build.abspath(),
            args=['install'])

        # we have written the fs to disk, but unfortunately we cannot
        # see what the build contributed to it (we don't implement
        # re-reading the fs that has changed under the hood)

        exe_path = install.abspath() + ['bin', 'explicit-name']
        self.failUnless(os.path.isfile(os.sep.join(exe_path)))
        
        pass
        
if __name__ == '__main__':
    unittest.TextTestRunner().run(ExecutableNameBuildSuite())
    pass

