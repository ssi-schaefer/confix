# Copyright (C) 2009 Joerg Faschingbauer

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

from libconfix.plugins.cmake.out_cmake import find_cmake_output_builder
from libconfix.plugins.cmake.setup import CMakeSetup

from libconfix.core.hierarchy.explicit_setup import ExplicitDirectorySetup
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.utils import const

import unittest

class HierarchyInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(HierarchyInMemoryTest('basic'))
        pass
    pass

class HierarchyInMemoryTest(unittest.TestCase):
    def basic(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("HierarchyInMemoryTest.basic")',
                              'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['DIRECTORY(["directory0"])',
                              'DIRECTORY(["directory1"])']))
        fs.rootdirectory().add(
            name='directory0',
            entry=Directory())
        fs.rootdirectory().add(
            name='directory1',
            entry=Directory())

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitDirectorySetup(), CMakeSetup()])
        package.boil(external_nodes=[])
        package.output()

        cmake_output_builder = find_cmake_output_builder(package.rootbuilder())

        print cmake_output_builder.local_cmakelists().subdirectories()
        self.failUnlessEqual(len(cmake_output_builder.local_cmakelists().subdirectories()), 2)
        self.failUnless('directory0' in cmake_output_builder.local_cmakelists().subdirectories())
        self.failUnless('directory1' in cmake_output_builder.local_cmakelists().subdirectories())

        pass

    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(HierarchyInMemorySuite())
    pass
