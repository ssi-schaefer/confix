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
from libconfix.core.utils import const

import unittest

class InterPackageInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(IntraPackageTest('test'))
        pass
    pass

class IntraPackageTest(unittest.TestCase):
    def setUp(self):
        # hi -> mid -> lo
        
        # this is our fixture
        self.__hi_package_local = None

        
        if True:
            lo_source = Directory()
            lo_source.add(
                name=const.CONFIX2_PKG,
                entry=File(lines=['PACKAGE_NAME("lo")',
                                  'PACKAGE_VERSION("1.2.3")']))
            lo_source.add(
                name=const.CONFIX2_DIR,
                entry=File(lines=['LIBRARY(basename="lo", members=[H(filename="lo.h"), C(filename="lo.c")])']))
            lo_source.add(
                name='lo.h',
                entry=File(lines=['#ifndef LO_H',
                                  '#define LO_H',
                                  'void lo();',
                                  '#endif']))
            lo_source.add(
                name='lo.c',
                entry=File(lines=['#include "lo.h"',
                                  'void lo() {}']))
            lo_package_local = LocalPackage(rootdirectory=lo_source,
                                            setups=[ExplicitDirectorySetup(),
                                                    ExplicitCSetup(),
                                                    CMakeSetup()])
            lo_package_local.boil(external_nodes=[])

            lo_package_installed = lo_package_local.install()
            pass

        if True:
            mid_source = Directory()
            mid_source.add(
                name=const.CONFIX2_PKG,
                entry=File(lines=['PACKAGE_NAME("mid")',
                                  'PACKAGE_VERSION("6.6.6")']))
            mid_source.add(
                name=const.CONFIX2_DIR,
                entry=File(lines=['LIBRARY(basename="mid", members=[H(filename="mid.h"), C(filename="mid.c")])']))
            mid_source.add(
                name='mid.h',
                entry=File(lines=['#ifndef MID_H',
                                  '#define MID_H',
                                  'void mid();',
                                  '#endif']))
            mid_source.add(
                name='mid.c',
                entry=File(lines=['#include "mid.h"',
                                  # spot bugs *really* early
                                  '// CONFIX:REQUIRE_H("lo.h", REQUIRED)',
                                  '#include <lo.h>',
                                  'void mid() { lo(); }']))
            mid_package_local = LocalPackage(rootdirectory=mid_source,
                                             setups=[ExplicitDirectorySetup(),
                                                     ExplicitCSetup(),
                                                     CMakeSetup()])
            mid_package_local.boil(external_nodes=lo_package_installed.nodes())

            mid_package_installed = mid_package_local.install()
            pass

        if True:
            hi_source = Directory()
            hi_source.add(
                name=const.CONFIX2_PKG,
                entry=File(lines=['PACKAGE_NAME("hi")',
                                  'PACKAGE_VERSION("2.3.4")']))
            hi_source.add(
                name=const.CONFIX2_DIR,
                entry=File(lines=['EXECUTABLE(exename="exe", center=C(filename="main.c"))']))
            hi_source.add(
                name='main.c',
                entry=File(lines=['#include <mid.h>',
                                  '#include <lo.h>',
                                  # spot bugs *really* early
                                  '// CONFIX:REQUIRE_H("mid.h", REQUIRED)',
                                  '// CONFIX:REQUIRE_H("lo.h", REQUIRED)',
                                  'int main(void) { mid(); }']))

            self.__hi_package_local = LocalPackage(rootdirectory=hi_source,
                                                   setups=[ExplicitDirectorySetup(),
                                                           ExplicitCSetup(),
                                                           CMakeSetup()])
            self.__hi_package_local.boil(external_nodes=mid_package_installed.nodes() + lo_package_installed.nodes())
            self.__hi_package_local.output()
            pass
            
        pass

    def test(self):
        output_builder = find_cmake_output_builder(self.__hi_package_local.rootbuilder())

        # hi uses two installed packages. nothing interesting with the
        # includes. we need only one path, pointing to the installed
        # include directory.
        include_directories = output_builder.local_cmakelists().get_include_directories()
        self.failUnlessEqual(len(include_directories), 1)
        self.failUnlessEqual(include_directories[0], '${CMAKE_INSTALL_PREFIX}/include')

        # boring with the library path as well.
        link_directories = output_builder.local_cmakelists().get_link_directories()
        self.failUnlessEqual(len(link_directories), 1)
        self.failUnlessEqual(link_directories[0], '${CMAKE_INSTALL_PREFIX}/lib')

        # more fun with the libraries.
        exe_target_link_libraries = output_builder.local_cmakelists().get_target_link_libraries('exe')
        self.failUnlessEqual(exe_target_link_libraries, ['mid', 'lo'])
        
        pass

    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(InterPackageInMemorySuite())
    pass
