# Copyright (C) 2007-2008 Joerg Faschingbauer

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

from libconfix.plugins.c.executable import ExecutableBuilder
from libconfix.plugins.c.h import HeaderBuilder
from libconfix.plugins.c.c import CBuilder
from libconfix.setups.explicit_setup import ExplicitSetup

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

import unittest

class ExecutableInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(ExecutableInMemoryTest('testExplicitName'))
        self.addTest(ExecutableInMemoryTest('testImplicitName'))
        pass
    pass

class ExecutableInMemoryTest(unittest.TestCase):
    def testExplicitName(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('ExecutableInMemoryTest')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["EXECUTABLE(exename='hansi', center=C(filename='main.c'), members=[])"]))
        fs.rootdirectory().add(
            name='main.c',
            entry=File())

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitSetup(use_libtool=False)])
        package.boil(external_nodes=[])

        found_exe_builder = None
        for b in package.rootbuilder().iter_builders():
            if isinstance(b, ExecutableBuilder):
                self.failUnless(found_exe_builder is None)
                found_exe_builder = b
                continue
            pass
        self.failIf(found_exe_builder is None)
        self.failUnless(found_exe_builder.exename() == 'hansi')
        pass

    def testImplicitName(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('ExecutableInMemoryTest')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["EXECUTABLE(center=C(filename='main.c'), members=[])"]))
        fs.rootdirectory().add(
            name='main.c',
            entry=File())

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitSetup(use_libtool=False)])
        package.boil(external_nodes=[])

        found_exe_builder = None
        for b in package.rootbuilder().iter_builders():
            if isinstance(b, ExecutableBuilder):
                self.failUnless(found_exe_builder is None)
                found_exe_builder = b
                continue
            pass
        self.failIf(found_exe_builder is None)
        self.failUnless(found_exe_builder.exename() == 'ExecutableInMemoryTest_main')
        pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(ExecutableInMemorySuite())
    pass

