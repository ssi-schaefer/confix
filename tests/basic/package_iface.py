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

from libconfix.core.setup import Setup
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.local_package import LocalPackage
from libconfix.core.utils import const

class PackageInterfaceSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(PackageInterfaceTest('test'))
        pass
    pass

class PackageInterfaceTest(unittest.TestCase):
    class DummySetup1(Setup): pass
    def test(self):
        fs = FileSystem(path=['dont\'t', 'care'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["from libconfix.core.setup import Setup",
                              "class DummySetup2(Setup): pass",
                              "PACKAGE_NAME('PackageInterfaceTest')",
                              "PACKAGE_VERSION('1.2.3')",
                              "ADD_SETUP(DummySetup2())"]))

        # add Confix2.dir for no real reason. we could really do
        # without, and should take some time to investigate. but not
        # now (now==2006-09-19).
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[PackageInterfaceTest.DummySetup1()])

        self.failUnlessEqual(package.name(), 'PackageInterfaceTest')
        self.failUnlessEqual(package.version(), '1.2.3')
        # we don't have DummySetup1's definition at hand (we defined
        # it inside Confix2.pkg), so we have to check for its name.
        self.failUnless(type(package.setups()[1]).__name__ != 'DummySetup1')
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(PackageInterfaceSuite())
    pass

