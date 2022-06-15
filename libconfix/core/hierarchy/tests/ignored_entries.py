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

from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.machinery.setup import Setup
from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.filebuilder import FileBuilder
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.frontends.confix2.confix_setup import ConfixSetup
from libconfix.core.utils import const

from libconfix.testutils import dirhier

import unittest

class IgnoreTestSetup(Setup):
    def setup(self, dirbuilder):
        dirbuilder.add_builder(IgnoreTestCreator())
        pass
    pass

class IgnoreTestCreator(Builder):
    def __init__(self):
        Builder.__init__(self)
        self.__seen_filenames = set()
        pass
    def locally_unique_id(self):
        # I am supposed to be the only one of my kind in any given
        # directory, so my class is a good unique ID.
        return str(self.__class__)
    def enlarge(self):
        for name, entry in self.parentbuilder().directory().entries():
            if name in self.__seen_filenames:
                continue
            self.__seen_filenames.add(name)
            if name.endswith('.ignoretest'):
                self.parentbuilder().add_builder(IgnoreTestBuilder(entry))
                pass
            pass
        pass
    pass

class IgnoreTestBuilder(FileBuilder): pass

class IgnoredEntries(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=['a'])
        fs.rootdirectory().add(name=const.CONFIX2_PKG,
                               entry=File(lines=["PACKAGE_NAME('ignore-entries-common')",
                                                 "PACKAGE_VERSION('6.6.6')"]))
        fs.rootdirectory().add(name=const.CONFIX2_DIR,
                               entry=File(lines=['IGNORE_ENTRIES(["ignored1.ignoretest"])',
                                                 'IGNORE_FILE("ignored2.ignoretest")']))
        fs.rootdirectory().add(name='ignored1.ignoretest',
                               entry=File())
        fs.rootdirectory().add(name='ignored2.ignoretest',
                               entry=File())
        fs.rootdirectory().add(name='not-ignored.ignoretest',
                               entry=File())
        
        package = LocalPackage(
            rootdirectory=fs.rootdirectory(),
            setups=[ConfixSetup(use_libtool=False),
                    IgnoreTestSetup()])
        package.boil(external_nodes=[])

        self.assertFalse(package.rootbuilder().find_entry_builder(path=['ignored1.ignoretest']))
        self.assertFalse(package.rootbuilder().find_entry_builder(path=['ignored2.ignoretest']))
        self.assertTrue(package.rootbuilder().find_entry_builder(path=['not-ignored.ignoretest']))

        pass

    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(IgnoredEntries)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
