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

import inter_package

from libconfix.plugins.cmake.out_cmake import find_cmake_output_builder
from libconfix.plugins.cmake.setup import CMakeSetup

from libconfix.plugins.c.setups.explicit_setup import ExplicitCSetup

from libconfix.core.hierarchy.explicit_setup import ExplicitDirectorySetup
from libconfix.core.machinery.local_package import LocalPackage

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

        source_tree = inter_package.make_source_tree()

        lo_source = source_tree.find(['lo'])
        lo_package_local = LocalPackage(rootdirectory=lo_source,
                                        setups=[ExplicitDirectorySetup(),
                                                ExplicitCSetup(),
                                                CMakeSetup()])
        lo_package_local.boil(external_nodes=[])
        lo_package_installed = lo_package_local.install()

        mid_source = source_tree.find(['mid'])
        mid_package_local = LocalPackage(rootdirectory=mid_source,
                                         setups=[ExplicitDirectorySetup(),
                                                 ExplicitCSetup(),
                                                 CMakeSetup()])
        mid_package_local.boil(external_nodes=lo_package_installed.nodes())
        mid_package_installed = mid_package_local.install()

        hi_source = source_tree.find(['hi'])
        self.__hi_package_local = LocalPackage(rootdirectory=hi_source,
                                               setups=[ExplicitDirectorySetup(),
                                                       ExplicitCSetup(),
                                                       CMakeSetup()])
        self.__hi_package_local.boil(external_nodes=mid_package_installed.nodes() + lo_package_installed.nodes())
        self.__hi_package_local.output()
            
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
