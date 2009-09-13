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
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.utils import const
from libconfix.testutils.persistent import PersistentTestCase

import unittest

class DependencyOrderInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(DependencyOrderTest('test'))
        pass
    pass

class DependencyOrderTest(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=[])
        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())

        # external definitions
        if True:
            externals = source.add(
                name='externals',
                entry=Directory())
            externals.add(
                name=const.CONFIX2_PKG,
                entry=File(lines=["PACKAGE_NAME('ext1')",
                                  "PACKAGE_VERSION('1.2.3')"]))
            externals.add(
                name=const.CONFIX2_DIR,
                entry=File(lines=["DIRECTORY(['ext1'])",
                                  "DIRECTORY(['ext2'])"]))

            ext1 = externals.add(
                name='ext1',
                entry=Directory())
            ext1.add(
                name=const.CONFIX2_DIR,
                entry=File(lines=["PROVIDE_SYMBOL('ext1')",
                                  "CMAKE_EXTERNAL_LIBRARY(",
                                  "    incpath=['ext1-incpath1', 'ext1-incpath2'],",
                                  "    libpath=['ext1-libpath1', 'ext1-libpath2'],",
                                  "    libs=['ext1-lib1', 'ext1-lib2'],",
                                  "    cmdlinemacros={'ext1-macro1': 'ext1-value1', 'ext1-macro2': None})"
                                  ]))
        
            ext2 = externals.add(
                name='ext2',
                entry=Directory())
            ext2.add(
                name=const.CONFIX2_DIR,
                entry=File(lines=["REQUIRE_SYMBOL('ext1', URGENCY_ERROR)",
                                  "PROVIDE_SYMBOL('ext2')",
                                  "CMAKE_EXTERNAL_LIBRARY(",
                                  "    incpath=['ext2-incpath1', 'ext2-incpath2'],",
                                  "    libpath=['ext2-libpath1', 'ext2-libpath2'],",
                                  "    libs=['ext2-lib1', 'ext2-lib2'],",
                                  "    cmdlinemacros={'ext2-macro1': 'ext2-value1', 'ext2-macro2': None})"
                                  ]))

            externals_package = LocalPackage(rootdirectory=externals,
                                             setups=[ExplicitDirectorySetup(), ExplicitCSetup(), CMakeSetup()])
            externals_package.boil(external_nodes=[])
            externals_package.output()
            externals_installed = externals_package.install()
            pass

        # native package #1
        if True:
            native1 = source.add(
                name='native1',
                entry=Directory())
            native1.add(
                name=const.CONFIX2_PKG,
                entry=File(lines=["PACKAGE_NAME('native1')",
                                  "PACKAGE_VERSION('1.2.3')"]))
            native1.add(
                name=const.CONFIX2_DIR,
                entry=File(lines=["REQUIRE_SYMBOL('ext2', URGENCY_ERROR)",
                                  "PROVIDE_SYMBOL('native1')",
                                  "LIBRARY(members=[H(filename='native1.h'), C(filename='native1.c')])"]))
            native1.add(
                name='native1.h',
                entry=File())
            native1.add(
                name='native1.c',
                entry=File())

            native1_package = LocalPackage(rootdirectory=native1,
                                           setups=[ExplicitDirectorySetup(), ExplicitCSetup(), CMakeSetup()])
            native1_package.boil(external_nodes=externals_installed.nodes())
            native1_installed = native1_package.install()
            pass
        
        # native package #2
        if True:
            native2 = source.add(
                name='native2',
                entry=Directory())
            native2.add(
                name=const.CONFIX2_PKG,
                entry=File(lines=["PACKAGE_NAME('native2')",
                                  "PACKAGE_VERSION('1.2.3')"]))
            native2.add(
                name=const.CONFIX2_DIR,
                entry=File(lines=["REQUIRE_SYMBOL('native1', URGENCY_ERROR)",
                                  "PROVIDE_SYMBOL('native2')",
                                  "LIBRARY(members=[H(filename='native2.h'), C(filename='native2.c')])"]))
            native2.add(
                name='native2.h',
                entry=File())
            native2.add(
                name='native2.c',
                entry=File())

            native2_package = LocalPackage(rootdirectory=native2,
                                           setups=[ExplicitDirectorySetup(), ExplicitCSetup(), CMakeSetup()])
            native2_package.boil(external_nodes=externals_installed.nodes()+native1_installed.nodes())
            native2_installed = native2_package.install()
            pass
        
        # final package
        if True:
            final = source.add(
                name='final',
                entry=Directory())
            final.add(
                name=const.CONFIX2_PKG,
                entry=File(lines=["PACKAGE_NAME('final')",
                                  "PACKAGE_VERSION('1.2.3')"]))
            final.add(
                name=const.CONFIX2_DIR,
                entry=File(lines=["DIRECTORY(['local1'])",
                                  "DIRECTORY(['local2'])",
                                  "DIRECTORY(['bin'])"]))

            local1 = final.add(
                name='local1',
                entry=Directory())
            local1.add(
                name=const.CONFIX2_DIR,
                entry=File(lines=["REQUIRE_SYMBOL('native2', URGENCY_ERROR)",
                                  "PROVIDE_SYMBOL('local1')",
                                  "LIBRARY(members=[C(filename='local1.c')])"]))
            local1.add(
                name='local1.c',
                entry=File())

            local2 = final.add(
                name='local2',
                entry=Directory())
            local2.add(
                name=const.CONFIX2_DIR,
                entry=File(lines=["REQUIRE_SYMBOL('local1', URGENCY_ERROR)",
                                  "PROVIDE_SYMBOL('local2')",
                                  "LIBRARY(members=[C(filename='local2.c')])"]))
            local2.add(
                name='local2.c',
                entry=File())

            bin = final.add(
                name='bin',
                entry=Directory())
            bin.add(
                name=const.CONFIX2_DIR,
                entry=File(lines=["REQUIRE_SYMBOL('local2', URGENCY_ERROR)",
                                  "EXECUTABLE(center=C(filename='main.c'))"]))
            bin.add(
                name='main.c',
                entry=File())

            final_package = LocalPackage(rootdirectory=final,
                                         setups=[ExplicitDirectorySetup(), ExplicitCSetup(), CMakeSetup()])
            final_package.boil(external_nodes=externals_installed.nodes()+native1_installed.nodes()+native2_installed.nodes())
            final_package.output()
            pass

        cmake_output_builder = find_cmake_output_builder(final_package.rootbuilder().find_entry_builder(['bin']))
        self.failUnlessEqual(cmake_output_builder.local_cmakelists().get_include_directories(),
                             ['${final_SOURCE_DIR}',
                              '${final_BINARY_DIR}',
                              '${CMAKE_INSTALL_PREFIX}',
                              'ext2-incpath1',
                              'ext2-incpath2',
                              'ext1-incpath1',
                              'ext1-incpath2'])

        self.fail() # -L, -l
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(DependencyOrderInMemorySuite())
    pass
