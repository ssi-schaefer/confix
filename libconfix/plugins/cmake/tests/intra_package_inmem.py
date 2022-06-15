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

from . import intra_package

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

class IntraPackageTest(unittest.TestCase):
    def setUp(self):
        fs = FileSystem(path=[], rootdirectory=intra_package.make_source_tree())
        
        self.__package = LocalPackage(rootdirectory=fs.rootdirectory(),
                                      setups=[ExplicitDirectorySetup(), ExplicitCSetup(), CMakeSetup()])
        self.__package.boil(external_nodes=[])
        self.__package.output()

        self.__lo_output_builder = find_cmake_output_builder(self.__package.rootbuilder().find_entry_builder(['lo']))
        self.__hi_output_builder = find_cmake_output_builder(self.__package.rootbuilder().find_entry_builder(['hi']))
        self.__exe_output_builder = find_cmake_output_builder(self.__package.rootbuilder().find_entry_builder(['exe']))
        pass

    def test__output(self):
        # library 'lo'
        self.assertEqual(len(self.__lo_output_builder.local_cmakelists().get_library('lo')), 4)
        self.assertTrue('lo1.h' in self.__lo_output_builder.local_cmakelists().get_library('lo'))
        self.assertTrue('lo1.c' in self.__lo_output_builder.local_cmakelists().get_library('lo'))
        self.assertTrue('lo2.h' in self.__lo_output_builder.local_cmakelists().get_library('lo'))
        self.assertTrue('lo2.c' in self.__lo_output_builder.local_cmakelists().get_library('lo'))

        # library 'hi'
        self.assertEqual(len(self.__hi_output_builder.local_cmakelists().get_library('hi')), 4)
        self.assertTrue('hi1.h' in self.__hi_output_builder.local_cmakelists().get_library('hi'))
        self.assertTrue('hi1.c' in self.__hi_output_builder.local_cmakelists().get_library('hi'))
        self.assertTrue('hi2.h' in self.__hi_output_builder.local_cmakelists().get_library('hi'))
        self.assertTrue('hi2.c' in self.__hi_output_builder.local_cmakelists().get_library('hi'))

        # executable 'exe'
        self.assertEqual(len(self.__exe_output_builder.local_cmakelists().get_executable('exe')), 5)
        self.assertTrue('main.c' in self.__exe_output_builder.local_cmakelists().get_executable('exe'))
        self.assertTrue('require_lo.h' in self.__exe_output_builder.local_cmakelists().get_executable('exe'))
        self.assertTrue('require_lo.c' in self.__exe_output_builder.local_cmakelists().get_executable('exe'))
        self.assertTrue('require_hi.h' in self.__exe_output_builder.local_cmakelists().get_executable('exe'))
        self.assertTrue('require_hi.c' in self.__exe_output_builder.local_cmakelists().get_executable('exe'))

        pass

    def test__linklines(self):
        # lo needs nothing.
        self.assertTrue(self.__lo_output_builder.local_cmakelists().get_target_link_libraries('lo') is None)

        # hi needs lo.
        hi_link_libraries = self.__hi_output_builder.local_cmakelists().get_target_link_libraries('hi')
        self.assertEqual(len(hi_link_libraries), 1)
        self.assertEqual(hi_link_libraries[0], 'lo')

        # exe need hi and lo, in that particular order.
        exe_link_libraries = self.__exe_output_builder.local_cmakelists().get_target_link_libraries('exe')
        self.assertEqual(len(exe_link_libraries), 2)
        self.assertEqual(exe_link_libraries[0], 'hi')
        self.assertEqual(exe_link_libraries[1], 'lo')

        pass

    def test__include_paths(self):
        self.assertEqual(len(self.__lo_output_builder.local_cmakelists().get_include_directories()),
                             # the binary directory that is associated with 'lo'
                             1
                             )

        hi_include_directories = self.__hi_output_builder.local_cmakelists().get_include_directories()
        self.assertEqual(len(hi_include_directories),
                             # the binary directory that is associated
                             # with 'hi', plus twice 'lo' (binary and
                             # source)
                             1 + 1*2)
        self.assertTrue(hi_include_directories[0] == '${CMAKE_CURRENT_BINARY_DIR}' and 
                        hi_include_directories[1] == '${'+self.__package.name()+'_SOURCE_DIR}/lo' and
                        hi_include_directories[2] == '${'+self.__package.name()+'_BINARY_DIR}/lo' or
                        hi_include_directories[1] == '${'+self.__package.name()+'_BINARY_DIR}/lo' and
                        hi_include_directories[2] == '${'+self.__package.name()+'_SOURCE_DIR}/lo')
        
        exe_include_directories = self.__exe_output_builder.local_cmakelists().get_include_directories()
        self.assertEqual(len(exe_include_directories),
                             # the binary directory that is
                             # associaated with 'exe', plus two each
                             # for 'hi' and 'lo'.
                             1 + 2*2)
        self.assertTrue(exe_include_directories[0] == '${CMAKE_CURRENT_BINARY_DIR}')
        self.assertTrue(exe_include_directories[1] == '${'+self.__package.name()+'_SOURCE_DIR}/hi' and
                        exe_include_directories[2] == '${'+self.__package.name()+'_BINARY_DIR}/hi' or
                        exe_include_directories[1] == '${'+self.__package.name()+'_BINARY_DIR}/hi' and
                        exe_include_directories[2] == '${'+self.__package.name()+'_SOURCE_DIR}/hi')
        self.assertTrue(exe_include_directories[3] == '${'+self.__package.name()+'_SOURCE_DIR}/lo' and
                        exe_include_directories[4] == '${'+self.__package.name()+'_BINARY_DIR}/lo' or
                        exe_include_directories[3] == '${'+self.__package.name()+'_BINARY_DIR}/lo' and
                        exe_include_directories[4] == '${'+self.__package.name()+'_SOURCE_DIR}/lo')

        pass

    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(IntraPackageTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
