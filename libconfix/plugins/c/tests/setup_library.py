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

from libconfix.plugins.c.h import HeaderBuilder
from libconfix.plugins.c.c import CBuilder
from libconfix.plugins.c.library import LibraryBuilder
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.machinery.filebuilder import FileBuilder
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const
from libconfix.testutils import dirhier
from libconfix.frontends.confix2.confix_setup import ConfixSetup

import unittest

class LibrarySetupBasic(unittest.TestCase):
    def test(self):
        fs = dirhier.packageroot()
        fs.rootdirectory().add(name='file.h', entry=File(lines=[]))
        fs.rootdirectory().add(name='file.c', entry=File(lines=[]))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])

        file_h_builder = None
        file_c_builder = None
        library_builder = None
        for b in package.rootbuilder().iter_builders():
            if isinstance(b, FileBuilder):
                if b.file().name() == 'file.h' and isinstance(b, HeaderBuilder):
                    file_h_builder = b
                    pass
                if b.file().name() == 'file.c' and isinstance(b, CBuilder):
                    file_c_builder = b
                    pass
                pass
            if isinstance(b, LibraryBuilder):
                library_builder = b
                pass
            pass
        self.assertTrue(isinstance(file_h_builder, HeaderBuilder))
        self.assertTrue(isinstance(file_c_builder, CBuilder)) 
        self.assertTrue(isinstance(library_builder, LibraryBuilder)) 

        self.assertTrue(file_h_builder in library_builder.members())
        self.assertTrue(file_c_builder in library_builder.members())
        pass
    pass

class LibraryNames(unittest.TestCase):
    def setUp(self):
        self.fs_ = dirhier.packageroot()
        dir1 = self.fs_.rootdirectory().add(name='dir1', entry=Directory())
        dir1.add(name=const.CONFIX2_DIR, entry=File(lines=[]))
        dir2 = dir1.add(name='dir2', entry=Directory())
        dir2.add(name=const.CONFIX2_DIR, entry=File(lines=[]))
        dir3 = dir2.add(name='dir3', entry=Directory())
        dir3.add(name=const.CONFIX2_DIR, entry=File(lines=[]))
        dir3.add(name='file.c', entry=File(lines=[]))
        self.dir3_ = dir3
        pass

    def testLongName(self):
        
        package = LocalPackage(rootdirectory=self.fs_.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])

        dir3lib_builder = None
        for b in package.rootbuilder().find_entry_builder(['dir1', 'dir2', 'dir3']).iter_builders():
            if isinstance(b, LibraryBuilder):
                self.assertFalse(dir3lib_builder is not None)
                dir3lib_builder = b
                pass
            pass

        self.assertEqual(dir3lib_builder.basename(),
                             '_'.join([package.name()]+self.dir3_.relpath(self.fs_.rootdirectory())))
        pass
    
    def testExplicitName(self):
        fs = FileSystem(path=['don\'t', 'care'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('LibraryNames.testExplicitName')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["LIBNAME('myownname')"]))
        fs.rootdirectory().add(
            name='file.c',
            entry=File())

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])

        for b in package.rootbuilder().iter_builders():
            if isinstance(b, LibraryBuilder):
                self.assertEqual(b.basename(), 'myownname')
                break
            pass
        else:
            self.fail()
            pass
        pass
    pass
    
suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(LibrarySetupBasic))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(LibraryNames))

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
