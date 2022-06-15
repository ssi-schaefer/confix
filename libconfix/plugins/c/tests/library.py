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

from libconfix.plugins.c.setups.default_setup import DefaultCSetup
from libconfix.plugins.c.library import LibraryBuilder
from libconfix.plugins.c.h import HeaderBuilder
from libconfix.plugins.c.c import CBuilder

from libconfix.core.hierarchy.implicit_setup import ImplicitDirectorySetup

from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

import unittest

class LibraryTest(unittest.TestCase):
    def test_library_members(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(name=const.CONFIX2_PKG,
                               entry=File(lines=['PACKAGE_NAME("Blah")',
                                                 'PACKAGE_VERSION("6.6.6")']))
        fs.rootdirectory().add(name=const.CONFIX2_DIR,
                               entry=File(lines=[]))
        liblo = fs.rootdirectory().add(name='lo', entry=Directory())
        liblo.add(name=const.CONFIX2_DIR, entry=File())
        liblo.add(name='lo.h', entry=File())
        liblo.add(name='lo.c', entry=File())
        
        package = LocalPackage(
            rootdirectory=fs.rootdirectory(),
            setups=[DefaultCSetup(), ImplicitDirectorySetup()])

        package.boil(external_nodes=[])

        lo_builder = package.rootbuilder().find_entry_builder(['lo'])
        lo_h_builder = package.rootbuilder().find_entry_builder(['lo', 'lo.h'])
        lo_c_builder = package.rootbuilder().find_entry_builder(['lo', 'lo.c'])
        self.assertFalse(lo_builder is None)
        self.assertFalse(lo_h_builder is None)
        self.assertFalse(lo_c_builder is None)

        lo_lib_builder = None
        for b in lo_builder.iter_builders():
            if isinstance(b, LibraryBuilder):
                if b.basename() == 'Blah_lo':
                    lo_lib_builder = b
                    break
                pass
            pass
        else:
            self.fail()
            pass

        self.assertTrue(lo_h_builder in lo_lib_builder.members())
        self.assertTrue(lo_c_builder in lo_lib_builder.members())
        pass

    pass

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(LibraryTest))

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
