# Copyright (C) 2009-2013 Joerg Faschingbauer

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

from libconfix.plugins.cmake.setup import CMakeSetup
from libconfix.plugins.cmake.out_cmake import find_cmake_output_builder
from libconfix.plugins.c.setups.explicit_setup import ExplicitCSetup
from libconfix.core.hierarchy.explicit_setup import ExplicitDirectorySetup
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.utils import const

import unittest

class ExternalLibraryTest(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=[])

        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('ExternalLibraryTest')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["DIRECTORY(['external'])",
                              "DIRECTORY(['linked'])"]))
        
        external = fs.rootdirectory().add(
            name='external',
            entry=Directory())
        external.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["PROVIDE_SYMBOL('the-external-library')",
                              "CMAKE_EXTERNAL_LIBRARY(",
                              "    cflags=['my-cflag1', 'my-cflag2'],",
                              "    cxxflags=['my-cxxflag1', 'my-cxxflag2'])",
                              ]))
        
        linked = fs.rootdirectory().add(
            name='linked',
            entry=Directory())
        linked.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["REQUIRE_SYMBOL('the-external-library', URGENCY_ERROR)",
                              "EXECUTABLE(center=C(filename='main.c'))"]))
        linked.add(
            name='main.c',
            entry=File(lines=["int main(void) {}"]))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitDirectorySetup(),
                                       ExplicitCSetup(),
                                       CMakeSetup()])
        package.boil(external_nodes=[])
        package.output()

        linked_cmake_output_builder = find_cmake_output_builder(package.rootbuilder().find_entry_builder(['linked']))
        self.assertTrue('my-cflag1' in linked_cmake_output_builder.local_cmakelists().get_definitions())
        self.assertTrue('my-cflag2' in linked_cmake_output_builder.local_cmakelists().get_definitions())
        self.assertTrue('my-cxxflag1' in linked_cmake_output_builder.local_cmakelists().get_definitions())
        self.assertTrue('my-cxxflag2' in linked_cmake_output_builder.local_cmakelists().get_definitions())
        pass
    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(ExternalLibraryTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
