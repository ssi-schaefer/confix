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

from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.utils import const

import unittest

class ToplevelBoilerplateTest(unittest.TestCase):
    def setUp(self):
        rootdirectory = Directory()
        rootdirectory.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("package-name")',
                              'PACKAGE_VERSION("1.2.3")']))            
        rootdirectory.add(
            name=const.CONFIX2_DIR,
            entry=File())
        package = LocalPackage(rootdirectory=rootdirectory,
                                      setups=[CMakeSetup()])
        package.boil(external_nodes=[])
        package.output()

        self.__cmakelists = find_cmake_output_builder(package.rootbuilder()).top_cmakelists()
        pass
    
    def test__basics(self):
        self.failUnlessEqual(self.__cmakelists.get_project(), 'package-name')
        self.failUnlessEqual(self.__cmakelists.get_set('VERSION'), '1.2.3')
        self.failUnlessEqual(self.__cmakelists.get_cmake_minimum_required('VERSION'), '2.6')
        pass

    def test__cpack(self):
        self.failUnless('CPack' in self.__cmakelists.get_includes())
        self.failUnlessEqual(self.__cmakelists.get_set('CPACK_SOURCE_PACKAGE_FILE_NAME'), '"${PROJECT_NAME}-${VERSION}"')
        self.failUnlessEqual(self.__cmakelists.get_set('CPACK_SOURCE_IGNORE_FILES'), "${CPACK_SOURCE_IGNORE_FILES};~\$")

        self.failUnlessEqual(self.__cmakelists.get_set('CPACK_PACKAGE_VERSION_MAJOR'), '1')
        self.failUnlessEqual(self.__cmakelists.get_set('CPACK_PACKAGE_VERSION_MINOR'), '2')
        self.failUnlessEqual(self.__cmakelists.get_set('CPACK_PACKAGE_VERSION_PATCH'), '3')
        pass

    def test__rpath(self):
        # RPATH settings, according to
        # http://www.vtk.org/Wiki/CMake_RPATH_handling. this ought to
        # be the way that we know from automake/libtool.

        # use, i.e. don't skip the full RPATH for the build tree
        self.failUnlessEqual(self.__cmakelists.get_set('CMAKE_SKIP_BUILD_RPATH'), 'FALSE')

        # when building, don't use the install RPATH already (but
        # later on when installing)
        self.failUnlessEqual(self.__cmakelists.get_set('CMAKE_BUILD_WITH_INSTALL_RPATH'), 'FALSE')

        # the RPATH to be used when installing
        self.failUnlessEqual(self.__cmakelists.get_set('CMAKE_INSTALL_RPATH'), "${CMAKE_INSTALL_PREFIX}/lib")

        # add the automatically determined parts of the RPATH which
        # point to directories outside the build tree to the install
        # RPATH
        self.failUnlessEqual(self.__cmakelists.get_set('CMAKE_INSTALL_RPATH_USE_LINK_PATH'), 'TRUE')
        pass
    
    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(ToplevelBoilerplateTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
