# Copyright (C) 2008-2012 Joerg Faschingbauer

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

from libconfix.frontends.confix2.confix_setup import ConfixSetup

from libconfix.plugins.c.library import LibraryBuilder

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

import unittest

class IgnoredEntriesTest(unittest.TestCase):
    def test_rootdirectory(self):
        fs = FileSystem(path=['a'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('ignore-entries-c-rootdirectory')",
                              "PACKAGE_VERSION('6.6.6')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['IGNORE_ENTRIES(["ignored.h"])',
                              'IGNORE_FILE("ignored.c")']))
        fs.rootdirectory().add(
            name='ignored.h',
            entry=File())
        fs.rootdirectory().add(
            name='ignored.c',
            entry=File())
        fs.rootdirectory().add(
            name='not-ignored.h',
            entry=File())
        
        package = LocalPackage(
            rootdirectory=fs.rootdirectory(),
            setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])

        self.assertFalse(package.rootbuilder().find_entry_builder(path=['ignored.h']))
        self.assertFalse(package.rootbuilder().find_entry_builder(path=['ignored.c']))
        self.assertTrue(package.rootbuilder().find_entry_builder(path=['not-ignored.h']))

        for librarybuilder in package.rootbuilder().iter_builders():
            if isinstance(librarybuilder, LibraryBuilder):
                break
            pass

        self.assertFalse('ignored.c' in (member.entry().name() for member in librarybuilder.members()))
        self.assertFalse('ignored.h' in (member.entry().name() for member in librarybuilder.members()))
        pass

    def test_subdirectory(self):
        fs = FileSystem(path=['a'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('ignore-entries-c-subdirectory')",
                              "PACKAGE_VERSION('6.6.6')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        subdirectory = fs.rootdirectory().add(
            name='subdirectory',
            entry=Directory())

        subdirectory.add(name=const.CONFIX2_DIR,
                         entry=File(lines=['IGNORE_ENTRIES(["ignored.h"])',
                                           'IGNORE_FILE("ignored.c")']))
        subdirectory.add(name='ignored.h',
                         entry=File())
        subdirectory.add(name='ignored.c',
                         entry=File())
        subdirectory.add(name='not-ignored.h',
                         entry=File())
        subdirectory.add(name='not-ignored.c',
                         entry=File())

        package = LocalPackage(
            rootdirectory=fs.rootdirectory(),
            setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])

        self.assertFalse(package.rootbuilder().find_entry_builder(path=['subdirectory', 'ignored.h']))
        self.assertFalse(package.rootbuilder().find_entry_builder(path=['subdirectory', 'ignored.c']))
        self.assertTrue(package.rootbuilder().find_entry_builder(path=['subdirectory', 'not-ignored.h']))
        self.assertTrue(package.rootbuilder().find_entry_builder(path=['subdirectory', 'not-ignored.c']))

        for librarybuilder in package.rootbuilder().find_entry_builder(['subdirectory']).iter_builders():
            if isinstance(librarybuilder, LibraryBuilder):
                break
            pass
        else:
            self.fail()
            pass

        self.assertFalse('ignored.c' in (member.entry().name() for member in librarybuilder.members()))
        self.assertFalse('ignored.h' in (member.entry().name() for member in librarybuilder.members()))
        pass
    pass

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(IgnoredEntriesTest))

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
