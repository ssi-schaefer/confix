# Copyright (C) 2007 Joerg Faschingbauer

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

from libconfix.testutils import find

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.utils import const
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.hierarchy.explicit_setup import ExplicitDirectorySetup

class ExplicitInterfaceInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(Without_Confix2_dir('test'))
        self.addTest(With_Confix2_dir('test'))
        pass
    pass

class Without_Confix2_dir(unittest.TestCase):

    """ See if 'subdir' is built when we explicitly say that it
    should. We do not add a Confix2.dir file to 'subdir'."""
    
    def test(self):
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
                               setups=[ExplicitDirectorySetup()])
        package.boil(external_nodes=[])

        self.failIf(find.find_entrybuilder(rootbuilder=package.rootbuilder(), path=['subdir']) is None)
        pass
    pass

class With_Confix2_dir(unittest.TestCase):

    """ Explicitly adding 'subdir' as subdirectory to be built, we
    check that an eventual Confix2.dir file is recognized an executed."""
    
    def test(self):
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
                               setups=[ExplicitDirectorySetup()])
        package.boil(external_nodes=[])

        self.failIf(find.find_entrybuilder(rootbuilder=package.rootbuilder(), path=['subdir']) is None)
        self.failUnlessEqual(dummy_property_receiver_file.get_property('the_property'), 'the_value')
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(ExplicitInterfaceInMemorySuite())
    pass
