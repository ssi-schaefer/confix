# Copyright (C) 2007-2013 Joerg Faschingbauer

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

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.utils import const
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.setups.explicit_setup import ExplicitSetup

class ExplicitInterfaceInMemoryTest(unittest.TestCase):
    def test__without_confix2_dir(self):

        # See if 'subdir' is built when we explicitly say that it
        # should. We do not add a Confix2.dir file to 'subdir'.
    
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["DIRECTORY(path=['subdir'])"]))
        fs.rootdirectory().add(
            name='subdir',
            entry=Directory())

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitSetup(use_libtool=True)])
        package.boil(external_nodes=[])

        self.failIf(package.rootbuilder().find_entry_builder(['subdir']) is None)
        pass

    def test__with_confix2_dir(self):
        
        # Explicitly adding 'subdir' as subdirectory to be built, we
        # check that an eventual Confix2.dir file is recognized an
        # executed.

        # This is done by adding a file to the subdirectory, and then
        # adding a file property to it from the subdir's Confix2.dir
        # file.
    
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["DIRECTORY(path=['subdir'])"]))
        subdir = fs.rootdirectory().add(
            name='subdir',
            entry=Directory())
        dummy_property_receiver_file = subdir.add(
            name='dummy_property_receiver_file',
            entry=File())
        subdir.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["SET_FILE_PROPERTY(filename='dummy_property_receiver_file',",
                              "                  name='the_property',",
                              "                  value='the_value')"]))
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitSetup(use_libtool=True)])
        package.boil(external_nodes=[])

        self.failIf(package.rootbuilder().find_entry_builder(['subdir']) is None)
        self.failUnlessEqual(dummy_property_receiver_file.get_property('the_property'), 'the_value')
        pass
    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(ExplicitInterfaceInMemoryTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
