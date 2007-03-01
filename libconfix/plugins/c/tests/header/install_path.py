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

from libconfix.plugins.c.setup import DefaultCSetup
from libconfix.plugins.c.h import HeaderBuilder

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.utils import const
from libconfix.core.machinery.local_package import LocalPackage

from libconfix.testutils import find

import unittest

class HeaderInstallPathInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(HeaderInstallPath('test_iface'))
        self.addTest(HeaderInstallPath('test_ambig1'))
        self.addTest(HeaderInstallPath('test_ambig2'))
        pass
    pass

class HeaderInstallPath(unittest.TestCase):
    def test_iface(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('HeaderInstallPath')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        fs.rootdirectory().add(
            name='file.h',
            entry=File(lines=["// CONFIX:INSTALLPATH('a/b')"]))
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[DefaultCSetup(use_libtool=False, short_libnames=False)])
        package.boil(external_nodes=[])
        file_h_builder = find.find_entrybuilder(rootbuilder=package.rootbuilder(), path=['file.h'])
        self.failUnlessEqual(file_h_builder.visible_in_directory(), ['a', 'b'])
        pass

    def test_ambig1(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('HeaderInstallPath')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())

        # ambiguity here
        file = fs.rootdirectory().add(
            name='file.h',
            entry=File(lines=["// CONFIX:INSTALLPATH('a/b')"]))
        file.set_property('INSTALLPATH_CINCLUDE', ['x'])

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[DefaultCSetup(use_libtool=False, short_libnames=False)])
        self.failUnlessRaises(HeaderBuilder.AmbiguousVisibility, package.boil, external_nodes=[])
        
        pass

    def test_ambig2(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('HeaderInstallPath')",
                              "PACKAGE_VERSION('1.2.3')"]))

        # ambiguity here
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['INSTALLDIR_H("x/y")']))
        file = fs.rootdirectory().add(
            name='file.h',
            entry=File())
        file.set_property('INSTALLPATH_CINCLUDE', ['x'])

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[DefaultCSetup(use_libtool=False, short_libnames=False)])
        self.failUnlessRaises(HeaderBuilder.AmbiguousVisibility, package.boil, external_nodes=[])
        
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(HeaderInstallPathInMemorySuite())
    pass

