# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2012 Joerg Faschingbauer

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
from libconfix.plugins.c.setups.default_setup import DefaultCSetup

from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

from libconfix.frontends.confix2.confix_setup import ConfixSetup

import unittest

class ExplicitLibraryVersionTest(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('ExplicitLibraryVersionTest')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["LIBRARY_VERSION((6,6,6))"]))
        fs.rootdirectory().add(
            name='file.c',
            entry=File())
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=True)])
        package.boil(external_nodes=[])

        for b in package.rootbuilder().iter_builders():
            if isinstance(b, LibraryBuilder):
                lib_builder = b
                break
            pass
        else:
            self.fail()
            pass

        self.failUnlessEqual(lib_builder.version(), (6,6,6))
        self.failUnlessEqual(lib_builder.default_version(), "1.2.3")
        pass
    pass

class DefaultLibraryVersionTest(unittest.TestCase):
    def make_package_and_return_library_builder(self, package_version):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('DefaultLibraryVersionTest')",
                              "PACKAGE_VERSION('"+package_version+"')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        fs.rootdirectory().add(
            name='file.c',
            entry=File())
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=True)])
        package.boil(external_nodes=[])

        for b in package.rootbuilder().iter_builders():
            if isinstance(b, LibraryBuilder):
                return b
            pass
        else:
            self.fail()
            pass
        pass
    pass

    def testExactPackageVersion(self):
        library_builder = self.make_package_and_return_library_builder('1.2.3')
        self.failUnless(library_builder.version() is None)
        self.failUnlessEqual(library_builder.default_version(), '1.2.3')
        pass
    def testPostfixedPackageVersion(self):
        library_builder = self.make_package_and_return_library_builder('2.0.0pre7')
        self.failUnless(library_builder.version() is None)
        self.failUnlessEqual(library_builder.default_version(), '2.0.0pre7')
        pass
    def testUnparseablePackageVersion(self):
        library_builder = self.make_package_and_return_library_builder('unparseable')
        self.failUnless(library_builder.version() is None)
        self.failUnlessEqual(library_builder.default_version(), 'unparseable')
        pass
    pass

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ExplicitLibraryVersionTest))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(DefaultLibraryVersionTest))

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
