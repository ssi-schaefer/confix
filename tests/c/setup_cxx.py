# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006 Joerg Faschingbauer

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

import unittest

from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.hierarchy.setup import DirectorySetup
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

from libconfix.testutils import find

from libconfix.plugins.c.setup import DefaultCSetup
from libconfix.plugins.c.library import LibraryBuilder
from libconfix.plugins.c.executable import ExecutableBuilder
from libconfix.plugins.c.cxx import CXXBuilder
from libconfix.plugins.c.h import HeaderBuilder

class CXXSetupSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(BasicCXXSetup('test'))
        self.addTest(HeadersOnlyMakeNoLibrary('test'))
        pass
    pass

class BasicCXXSetup(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=['', 'path', 'to', 'package'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('BasicCXXSetup')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())

        lib = fs.rootdirectory().add(
            name='lib',
            entry=Directory())
        lib.add(
            name=const.CONFIX2_DIR,
            entry=File())
        lib.add(
            name='lib.h',
            entry=File())
        lib.add(
            name='lib.cc',
            entry=File())
        
        exe = fs.rootdirectory().add(
            name='exe',
            entry=Directory())
        exe.add(
            name=const.CONFIX2_DIR,
            entry=File())
        exe.add(
            name='main.cc',
            entry=File(lines=['void main() {}']))
        
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[DirectorySetup(),
                                       DefaultCSetup(use_libtool=False,
                                                     short_libnames=False)])
        package.boil(external_nodes=[])
        package.output()

        lib_dirbuilder = find.find_entrybuilder(package.rootbuilder(), ['lib'])
        exe_dirbuilder = find.find_entrybuilder(package.rootbuilder(), ['exe'])

        self.failIf(lib_dirbuilder is None)
        self.failIf(exe_dirbuilder is None)

        for b in lib_dirbuilder.builders():
            if isinstance(b, LibraryBuilder):
                found_lib_h = False
                found_lib_cc = False
                for member in b.members():
                    if isinstance(member, HeaderBuilder) and member.file().name() == 'lib.h':
                        found_lib_h = True
                        continue
                    if isinstance(member, CXXBuilder) and member.file().name() == 'lib.cc':
                        found_lib_cc = True
                        continue
                    pass
                self.failUnless(found_lib_h)
                self.failUnless(found_lib_cc)
                break
            pass
        else:
            self.fail()
            pass

        for b in exe_dirbuilder.builders():
            if isinstance(b, ExecutableBuilder):
                self.failUnless(isinstance(b.center(), CXXBuilder) and b.center().file().name() == 'main.cc')
                self.failUnlessEqual(len(b.members()), 1)
                break
            pass
        else:
            self.fail()
            pass
        pass
    pass

class HeadersOnlyMakeNoLibrary(unittest.TestCase):

    # if a directory contains only header file and no real code,
    # there's no need to build a library there.
    
    def test(self):
        fs = FileSystem(path=['', 'path', 'to', 'package'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('HeadersOnlyMakesNoLibrary')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())

        fs.rootdirectory().add(
            name='file.h',
            entry=File())

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[DefaultCSetup(use_libtool=False, short_libnames=False)])
        package.boil(external_nodes=[])

        for b in package.rootbuilder().builders():
            if isinstance(b, LibraryBuilder):
                self.fail()
                pass
            pass
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(CXXSetupSuite())
    pass

