# Copyright (C) 2007 Joerg Faschingbauer

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

from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.utils import const
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.plugins.c.setups.explicit_setup import ExplicitCSetup
from libconfix.plugins.c.executable import ExecutableBuilder
from libconfix.plugins.c.library import LibraryBuilder

import unittest

class LibtoolInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(LibtoolInMemoryTest('testLibrary'))
        self.addTest(LibtoolInMemoryTest('testExecutable'))
        pass
    pass

class LibtoolInMemoryTest(unittest.TestCase):
    def testLibrary(self):
        rootdir = Directory()
        rootdir.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('LibtoolInMemoryTest.testLibrary')",
                              "PACKAGE_VERSION('1.2.3')"]))
        rootdir.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["LIBRARY(members=[C(filename='file.c')])"]))
        rootdir.add(
            name='file.c',
            entry=File())

        package = LocalPackage(rootdirectory=rootdir,
                               setups=[ExplicitCSetup(use_libtool=True)])
        package.boil(external_nodes=[])

        library_builder = None
        for b in package.rootbuilder().builders():
            if isinstance(b, LibraryBuilder):
                self.failUnless(library_builder is None)
                library_builder = b
                pass
            pass
        self.failUnless(library_builder.use_libtool())
        pass

    def testExecutable(self):
        rootdir = Directory()
        rootdir.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('LibtoolInMemoryTest.testExecutable')",
                              "PACKAGE_VERSION('1.2.3')"]))
        rootdir.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["EXECUTABLE(center=C(filename='file.c'))"]))
        rootdir.add(
            name='file.c',
            entry=File())

        package = LocalPackage(rootdirectory=rootdir,
                               setups=[ExplicitCSetup(use_libtool=True)])
        package.boil(external_nodes=[])

        exe_builder = None
        for b in package.rootbuilder().builders():
            if isinstance(b, ExecutableBuilder):
                self.failUnless(exe_builder is None)
                exe_builder = b
                pass
            pass
        self.failUnless(exe_builder.use_libtool())
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(LibtoolInMemorySuite())
    pass

