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

from libconfix.plugins.c.setups.explicit_setup import ExplicitCSetup

from libconfix.core.hierarchy.explicit_setup import ExplicitDirectorySetup
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.utils import const

import unittest

class LibraryInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(LibraryTest('single_library'))
        self.addTest(LibraryTest('library_with_native_local_dependencies'))
        self.addTest(LibraryTest('library_with_native_foreign_dependencies'))
        self.addTest(LibraryTest('library_with_external_dependencies'))
        pass
    pass

class LibraryTest(unittest.TestCase):
    def single_library(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(name=const.CONFIX2_PKG,
                               entry=File(lines=['PACKAGE_NAME("LibraryTest.basic_test")',
                                                 'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(name=const.CONFIX2_DIR,
                               entry=File(lines=['LIBRARY(basename="the-library",',
                                                 '        members=[C(filename="file.c"),',
                                                 '                 H(filename="file.h")])']))
        fs.rootdirectory().add(name='file.h',
                               entry=File())
        fs.rootdirectory().add(name='file.c',
                               entry=File())

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitDirectorySetup(), ExplicitCSetup(), CMakeSetup()])
        package.boil(external_nodes=[])
        package.output()

        cmake_output_builder = find_cmake_output_builder(package.rootbuilder())
        self.failIf(cmake_output_builder is None)

        # see if we have the library defined with all its members.
        library_definition = cmake_output_builder.local_cmakelists().get_library_definition('the-library')
        self.failIf(library_definition is None)

        self.failUnless('file.h' in library_definition)
        self.failUnless('file.c' in library_definition)

        # see if CMakeLists.txt has been written.
        self.failUnless(fs.rootdirectory().get('CMakeLists.txt'))

        pass

    def library_with_native_local_dependencies(self):
        self.fail()
        pass

    def library_with_native_foreign_dependencies(self):
        self.fail()
        pass

    def library_with_external_dependencies(self):
        self.fail()
        pass

    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(LibraryInMemorySuite())
    pass
