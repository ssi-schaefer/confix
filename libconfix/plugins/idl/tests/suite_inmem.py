# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2013 Joerg Faschingbauer

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

from libconfix.plugins.idl.setup import IDLSetup

from libconfix.frontends.confix2.confix_setup import ConfixSetup

from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

import unittest

class IDLTest(unittest.TestCase):
    def test__basic(self):
        fs = FileSystem(path=['don\'t', 'care'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('BasicIDLTest')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())

        fs.rootdirectory().add(
            name='file.idl',
            entry=File(lines=["module A {",
                              "  module B {",
                              "    // ...",
                              "  }; // /module",
                              "}; // /module"]))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[IDLSetup()])
        package.boil(external_nodes=[])
        idl_builder = package.rootbuilder().find_entry_builder(['file.idl'])
        self.failIf(idl_builder is None)
        self.failUnlessEqual(idl_builder.install_path(), ['A', 'B'])
        pass

    def test__no_internal_requires(self):
        fs = FileSystem(path=['don\'t', 'care'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('BasicIDLTest')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())

        fs.rootdirectory().add(
            name='file1.idl',
            entry=File(lines=["#include <file2.idl>"]))
        fs.rootdirectory().add(
            name='file2.idl',
            entry=File())

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[IDLSetup()])
        package.boil(external_nodes=[])
        self.failIf(len(package.rootbuilder().requires()) != 0)
        pass

    def test__module_not_closed_is_flat(self):
        fs = FileSystem(path=['don\'t', 'care'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('ModuleNotClosedIsFlat')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())

        fs.rootdirectory().add(
            name='file.idl',
            entry=File(lines=["module A {",
                              "};"]))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[IDLSetup()])
        package.boil(external_nodes=[])
        idl_builder = package.rootbuilder().find_entry_builder(['file.idl'])
        self.failIf(idl_builder is None)
        self.failUnlessEqual(idl_builder.install_path(), [])
        pass

    def test__creator(self):
        fs = FileSystem(path=['a'])
        fs.rootdirectory().add(name=const.CONFIX2_PKG,
                               entry=File(lines=["PACKAGE_NAME('ignore-entries-c')",
                                                 "PACKAGE_VERSION('6.6.6')"]))
        fs.rootdirectory().add(name=const.CONFIX2_DIR,
                               entry=File(lines=['IGNORE_ENTRIES(["ignored1.idl"])',
                                                 'IGNORE_FILE("ignored2.idl")']))
        fs.rootdirectory().add(name='ignored1.idl',
                               entry=File())
        fs.rootdirectory().add(name='ignored2.idl',
                               entry=File())
        fs.rootdirectory().add(name='not-ignored.idl',
                               entry=File())
        
        package = LocalPackage(
            rootdirectory=fs.rootdirectory(),
            setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])

        self.failIf(package.rootbuilder().find_entry_builder(path=['ignored1.idl']))
        self.failIf(package.rootbuilder().find_entry_builder(path=['ignored2.idl']))
        self.failUnless(package.rootbuilder().find_entry_builder(path=['not-ignored.idl']))
        pass
    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(IDLTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
