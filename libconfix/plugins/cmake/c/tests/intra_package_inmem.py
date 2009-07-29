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

class IntraPackageInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(IntraPackageTest('single_library'))
        self.addTest(IntraPackageTest('libraries_with_native_local_dependencies'))
        self.addTest(IntraPackageTest('library_with_native_foreign_dependencies'))
        self.addTest(IntraPackageTest('library_with_external_dependencies'))
        pass
    pass

class IntraPackageTest(unittest.TestCase):
    def single_library(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("LibraryTest.basic_test")',
                              'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['LIBRARY(basename="the-library",',
                              '        members=[C(filename="file.c"),',
                              '                 H(filename="file.h")])']))
        fs.rootdirectory().add(
            name='file.h',
            entry=File())
        fs.rootdirectory().add(
            name='file.c',
            entry=File())

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitDirectorySetup(), ExplicitCSetup(), CMakeSetup()])
        package.boil(external_nodes=[])
        package.output()

        cmake_output_builder = find_cmake_output_builder(package.rootbuilder())
        self.failIf(cmake_output_builder is None)

        # see if we have the library defined with all its members.
        library = cmake_output_builder.local_cmakelists().get_library('the-library')
        self.failIf(library is None)

        self.failUnless('file.h' in library)
        self.failUnless('file.c' in library)

        # see if CMakeLists.txt has been written.
        self.failUnless(fs.rootdirectory().get('CMakeLists.txt'))

        pass

    def libraries_with_native_local_dependencies(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("LibraryTest.basic_test")',
                              'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['DIRECTORY(["lo"])',
                              'DIRECTORY(["hi"])',
                              'DIRECTORY(["hiest"])']))
        lo = fs.rootdirectory().add(
            name='lo',
            entry=Directory())
        lo.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['LIBRARY(basename="lo",',
                              '        members=[C(filename="lo.c"),',
                              '                 H(filename="lo.h")])']))
        lo.add(
            name='lo.h',
            entry=File())
        lo.add(
            name='lo.c',
            entry=File())
        
        hi = fs.rootdirectory().add(
            name='hi',
            entry=Directory())
        hi.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['LIBRARY(basename="hi",',
                              '        members=[C(filename="hi.c"),',
                              '                 H(filename="hi.h")])']))
        hi.add(
            name='hi.h',
            entry=File())
        hi.add(
            name='hi.c',
            entry=File(lines=['#include <lo.h>']))

        hiest = fs.rootdirectory().add(
            name='hiest',
            entry=Directory())
        hiest.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['LIBRARY(basename="hiest",',
                              '        members=[C(filename="hiest.c"),',
                              '                 H(filename="hiest.h")])']))
        hiest.add(
            name='hiest.h',
            entry=File())
        hiest.add(
            name='hiest.c',
            entry=File(lines=['#include <hi.h>']))
        
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitDirectorySetup(), ExplicitCSetup(), CMakeSetup()])
        package.boil(external_nodes=[])
        package.output()

        lo_output_builder = find_cmake_output_builder(package.rootbuilder().find_entry_builder(['lo']))
        hi_output_builder = find_cmake_output_builder(package.rootbuilder().find_entry_builder(['hi']))
        hiest_output_builder = find_cmake_output_builder(package.rootbuilder().find_entry_builder(['hiest']))

        # hiest -> hi -> lo
        lo_link_libraries = lo_output_builder.local_cmakelists().get_target_link_libraries('lo')
        self.failUnless(lo_link_libraries is None)

        hi_link_libraries = hi_output_builder.local_cmakelists().get_target_link_libraries('hi')
        self.failUnlessEqual(len(hi_link_libraries), 1)
        self.failUnlessEqual(hi_link_libraries[0], 'lo')

        hiest_link_libraries = hiest_output_builder.local_cmakelists().get_target_link_libraries('hiest')
        self.failUnlessEqual(len(hiest_link_libraries), 2)
        self.failUnlessEqual(hiest_link_libraries[0], 'hi')
        self.failUnlessEqual(hiest_link_libraries[1], 'lo')
        
        pass

    def library_with_native_foreign_dependencies(self):
        self.fail()
        pass

    def library_with_external_dependencies(self):
        self.fail()
        pass

    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(IntraPackageInMemorySuite())
    pass
