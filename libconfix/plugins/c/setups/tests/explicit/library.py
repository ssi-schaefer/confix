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

from libconfix.plugins.c.library import LibraryBuilder
from libconfix.plugins.c.h import HeaderBuilder
from libconfix.plugins.c.c import CBuilder
from libconfix.plugins.c.setups.explicit_setup import ExplicitCSetup

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

import unittest

class LibraryInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(LibraryInMemoryTest('testExplicitName'))
        self.addTest(LibraryInMemoryTest('testLongMangledName'))
        self.addTest(LibraryInMemoryTest('testMembers'))
        pass
    pass

class LibraryInMemoryTest(unittest.TestCase):
    def testExplicitName(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('LibraryInMemoryTest')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["LIBRARY(basename='hansi', members=[])"]))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitCSetup(use_libtool=False)])
        package.boil(external_nodes=[])

        found_lib_builder = None
        for b in package.rootbuilder().builders():
            if type(b) is LibraryBuilder:
                self.failUnless(found_lib_builder is None)
                found_lib_builder = b
                continue
            pass
        self.failIf(found_lib_builder is None)
        self.failUnless(found_lib_builder.basename() == 'hansi')
        pass

    def testLongMangledName(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('LibraryInMemoryTest')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["LIBRARY(members=[])"]))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitCSetup(use_libtool=False)])
        package.boil(external_nodes=[])

        found_lib_builder = None
        for b in package.rootbuilder().builders():
            if type(b) is LibraryBuilder:
                self.failUnless(found_lib_builder is None)
                found_lib_builder = b
                continue
            pass
        self.failIf(found_lib_builder is None)
        self.failUnless(found_lib_builder.basename() == 'LibraryInMemoryTest')
        pass

    def testMembers(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('LibraryInMemoryTest')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["LIBRARY(members=[H(filename='member1.h'),",
                              "                 H(filename='member2.h'),",
                              "                 C(filename='member1.c'),",
                              "                 C(filename='member2.c')])"]))
        fs.rootdirectory().add(
            name='member1.h',
            entry=File())
        fs.rootdirectory().add(
            name='member2.h',
            entry=File())
        fs.rootdirectory().add(
            name='member1.c',
            entry=File())
        fs.rootdirectory().add(
            name='member2.c',
            entry=File())

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitCSetup(use_libtool=False)])
        package.boil(external_nodes=[])

        found_lib_builder = None
        for b in package.rootbuilder().builders():
            if type(b) is LibraryBuilder:
                self.failUnless(found_lib_builder is None)
                found_lib_builder = b
                continue
            pass

        # see if the library contains what we asked it for.
        found_h1 = found_h2 = found_c1 = found_c2 = None
        for b in found_lib_builder.members():
            if isinstance(b, HeaderBuilder) and b.file().name() == 'member1.h':
                self.failUnless(found_h1 is None)
                found_h1 = b
                continue
            if isinstance(b, HeaderBuilder) and b.file().name() == 'member2.h':
                self.failUnless(found_h2 is None)
                found_h2 = b
                continue
            if isinstance(b, CBuilder) and b.file().name() == 'member1.c':
                self.failUnless(found_c1 is None)
                found_c1 = b
                continue
            if isinstance(b, CBuilder) and b.file().name() == 'member2.c':
                self.failUnless(found_c2 is None)
                found_c2 = b
                continue
            pass

        self.failIf(found_h1 is None)
        self.failIf(found_h2 is None)
        self.failIf(found_c1 is None)
        self.failIf(found_c2 is None)

        # we created the library's member builders using the C and H
        # 'macros' which should have added them to the containing
        # directory builder as a side effect.
        found_h1 = found_h2 = found_c1 = found_c2 = None
        for b in package.rootbuilder().builders():
            if isinstance(b, HeaderBuilder) and b.file().name() == 'member1.h':
                self.failUnless(found_h1 is None)
                found_h1 = b
                continue
            if isinstance(b, HeaderBuilder) and b.file().name() == 'member2.h':
                self.failUnless(found_h2 is None)
                found_h2 = b
                continue
            if isinstance(b, CBuilder) and b.file().name() == 'member1.c':
                self.failUnless(found_c1 is None)
                found_c1 = b
                continue
            if isinstance(b, CBuilder) and b.file().name() == 'member2.c':
                self.failUnless(found_c2 is None)
                found_c2 = b
                continue
            pass

        self.failIf(found_h1 is None)
        self.failIf(found_h2 is None)
        self.failIf(found_c1 is None)
        self.failIf(found_c2 is None)
        
        pass

    pass
        
if __name__ == '__main__':
    unittest.TextTestRunner().run(LibraryInMemorySuite())
    pass
