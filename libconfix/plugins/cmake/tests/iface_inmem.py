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

from libconfix.plugins.cmake.setup import CMakeSetup
from libconfix.plugins.cmake.out_cmake import find_cmake_output_builder
from libconfix.plugins.cmake.external_library import ExternalLibraryBuilder
from libconfix.plugins.cmake.external_library import BuildInfo_IncludePath_External_CMake
from libconfix.plugins.cmake.external_library import BuildInfo_LibraryPath_External_CMake
from libconfix.plugins.cmake.external_library import BuildInfo_Toplevel_CMakeLists_Include
from libconfix.plugins.cmake.external_library import BuildInfo_Toplevel_CMakeLists_FindCall
from libconfix.plugins.cmake.external_library import BuildInfo_Library_External_CMake
from libconfix.plugins.cmake.external_library import BuildInfo_CommandlineMacros_CMake

from libconfix.core.hierarchy.explicit_setup import ExplicitDirectorySetup
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.utils import const

import itertools
import unittest

class InterfaceInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(InterfaceInMemoryTest('test_CMAKE_ADD_CONFIX_MODULE'))
        self.addTest(InterfaceInMemoryTest('test_CMAKE_CMAKELISTS_ADD_INCLUDE_local_only'))
        self.addTest(InterfaceInMemoryTest('test_CMAKE_CMAKELISTS_ADD_INCLUDE_propagate_only'))
        self.addTest(InterfaceInMemoryTest('test_CMAKE_CMAKELISTS_ADD_INCLUDE_propagate_and_local'))
        self.addTest(InterfaceInMemoryTest('test_CMAKE_CMAKELISTS_ADD_FIND_CALL_local_only'))
        self.addTest(InterfaceInMemoryTest('test_CMAKE_CMAKELISTS_ADD_FIND_CALL_propagate_only'))
        self.addTest(InterfaceInMemoryTest('test_CMAKE_CMAKELISTS_ADD_FIND_CALL_propagate_and_local'))
        self.addTest(InterfaceInMemoryTest('test_CMAKE_EXTERNAL_LIBRARY'))
        pass
    pass

class InterfaceInMemoryTest(unittest.TestCase):
    def test_CMAKE_ADD_CONFIX_MODULE(self):
        fs = FileSystem(path=[''])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("test_CMAKE_ADD_CONFIX_MODULE")',
                              'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['CMAKE_ADD_CONFIX_MODULE(',
                              '    name="file1",',
                              '    lines=["xxx"])',
                              'CMAKE_ADD_CONFIX_MODULE(',
                              '    name="file2",',
                              '    lines=["xxx"])']))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitDirectorySetup(), CMakeSetup()])
        package.boil(external_nodes=[])
        package.output()

        self.failUnless(fs.rootdirectory().find(['confix-admin', 'cmake', 'Modules', 'file1']))
        self.failUnless(fs.rootdirectory().find(['confix-admin', 'cmake', 'Modules', 'file2']))
        
        pass

    def test_CMAKE_CMAKELISTS_ADD_INCLUDE_local_only(self):
        fs = FileSystem(path=[''])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("test_CMAKE_CMAKELISTS_ADD_INCLUDE_local_only")',
                              'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['CMAKE_CMAKELISTS_ADD_INCLUDE("include1", CMAKE_BUILDINFO_LOCAL)',
                              'CMAKE_CMAKELISTS_ADD_INCLUDE("include2", CMAKE_BUILDINFO_LOCAL)']))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitDirectorySetup(), CMakeSetup()])
        package.boil(external_nodes=[])
        package.output()

        self.failUnless('include1' in find_cmake_output_builder(package.rootbuilder()).top_cmakelists().get_includes())
        self.failUnless('include2' in find_cmake_output_builder(package.rootbuilder()).top_cmakelists().get_includes())

        for buildinfo in package.rootbuilder().buildinfos():
            self.failIf(isinstance(buildinfo, BuildInfo_Toplevel_CMakeLists_Include))
            pass
        pass

    def test_CMAKE_CMAKELISTS_ADD_INCLUDE_propagate_only(self):
        fs = FileSystem(path=[''])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("test_CMAKE_CMAKELISTS_ADD_INCLUDE_propagate_only")',
                              'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['CMAKE_CMAKELISTS_ADD_INCLUDE("include", CMAKE_BUILDINFO_PROPAGATE)']))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitDirectorySetup(), CMakeSetup()])
        package.boil(external_nodes=[])
        package.output()

        self.failIf('include' in find_cmake_output_builder(package.rootbuilder()).top_cmakelists().get_includes())

        for buildinfo in package.rootbuilder().buildinfos():
            if isinstance(buildinfo, BuildInfo_Toplevel_CMakeLists_Include):
                break
            pass
        else:
            self.fail()
            pass
        pass

    def test_CMAKE_CMAKELISTS_ADD_INCLUDE_propagate_and_local(self):
        fs = FileSystem(path=[''])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("test_CMAKE_CMAKELISTS_ADD_INCLUDE_propagate_and_local")',
                              'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['CMAKE_CMAKELISTS_ADD_INCLUDE("include", (CMAKE_BUILDINFO_LOCAL, CMAKE_BUILDINFO_PROPAGATE))']))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitDirectorySetup(), CMakeSetup()])
        package.boil(external_nodes=[])
        package.output()

        self.failUnless('include' in find_cmake_output_builder(package.rootbuilder()).top_cmakelists().get_includes())

        for buildinfo in package.rootbuilder().buildinfos():
            if isinstance(buildinfo, BuildInfo_Toplevel_CMakeLists_Include):
                break
            pass
        else:
            self.fail()
            pass
        pass

    def test_CMAKE_CMAKELISTS_ADD_FIND_CALL_local_only(self):
        fs = FileSystem(path=[''])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("test_CMAKE_CMAKELISTS_ADD_FIND_CALL_local_only")',
                              'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['CMAKE_CMAKELISTS_ADD_FIND_CALL("call1", CMAKE_BUILDINFO_LOCAL)',
                              'CMAKE_CMAKELISTS_ADD_FIND_CALL("call2", CMAKE_BUILDINFO_LOCAL)']))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitDirectorySetup(), CMakeSetup()])
        package.boil(external_nodes=[])
        package.output()

        self.failUnless('call1' in find_cmake_output_builder(package.rootbuilder()).top_cmakelists().get_find_calls())
        self.failUnless('call2' in find_cmake_output_builder(package.rootbuilder()).top_cmakelists().get_find_calls())

        for buildinfo in package.rootbuilder().buildinfos():
            self.failIf(isinstance(buildinfo, BuildInfo_Toplevel_CMakeLists_FindCall))
            pass
        pass

    def test_CMAKE_CMAKELISTS_ADD_FIND_CALL_propagate_only(self):
        fs = FileSystem(path=[''])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("test_CMAKE_CMAKELISTS_ADD_FIND_CALL_propagate_only")',
                              'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['CMAKE_CMAKELISTS_ADD_FIND_CALL("call", CMAKE_BUILDINFO_PROPAGATE)']))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitDirectorySetup(), CMakeSetup()])
        package.boil(external_nodes=[])
        package.output()

        self.failIf('call' in find_cmake_output_builder(package.rootbuilder()).top_cmakelists().get_find_calls())

        for buildinfo in package.rootbuilder().buildinfos():
            if isinstance(buildinfo, BuildInfo_Toplevel_CMakeLists_FindCall):
                break
            pass
        else:
            self.fail()
            pass
        pass

    def test_CMAKE_CMAKELISTS_ADD_FIND_CALL_propagate_and_local(self):
        fs = FileSystem(path=[''])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("test_CMAKE_CMAKELISTS_ADD_FIND_CALL_propagate_and_local")',
                              'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['CMAKE_CMAKELISTS_ADD_FIND_CALL("call", (CMAKE_BUILDINFO_PROPAGATE, CMAKE_BUILDINFO_LOCAL))']))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitDirectorySetup(), CMakeSetup()])
        package.boil(external_nodes=[])
        package.output()

        self.failUnless('call' in find_cmake_output_builder(package.rootbuilder()).top_cmakelists().get_find_calls())

        for buildinfo in package.rootbuilder().buildinfos():
            if isinstance(buildinfo, BuildInfo_Toplevel_CMakeLists_FindCall):
                break
            pass
        else:
            self.fail()
            pass
        pass

    def test_CMAKE_EXTERNAL_LIBRARY(self):
        fs = FileSystem(path=[''])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("test_CMAKE_CMAKELISTS_ADD_INCLUDE")',
                              'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["CMAKE_EXTERNAL_LIBRARY(",
                              "    incpath=['includedir1', 'includedir2'],",
                              "    libpath=['libdir1', 'libdir2'],",
                              "    libs=['lib1', 'lib2'],",
                              "    cmdlinemacros={'macro1': 'value1',",
                              "                   'macro2': 'value2'})"]))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitDirectorySetup(), CMakeSetup()])
        package.boil(external_nodes=[])
        package.output()

        external_library_builders = []
        for external_library_builder in package.rootbuilder().iter_builders():
            if isinstance(external_library_builder, ExternalLibraryBuilder):
                external_library_builders.append(external_library_builder)
                pass
            pass
        self.failUnlessEqual(len(external_library_builders), 1)

        incpath_infos = []
        for incpath_info in external_library_builders[0].buildinfos():
            if isinstance(incpath_info, BuildInfo_IncludePath_External_CMake):
                incpath_infos.append(incpath_info)
                pass
            pass
        self.failUnlessEqual(len(incpath_infos), 1)
        self.failUnlessEqual(incpath_infos[0].incpath(), ['includedir1', 'includedir2'])

        libpath_infos = []
        for libpath_info in external_library_builders[0].buildinfos():
            if isinstance(libpath_info, BuildInfo_LibraryPath_External_CMake):
                libpath_infos.append(libpath_info)
                pass
            pass
        self.failUnlessEqual(len(libpath_infos), 1)
        self.failUnlessEqual(libpath_infos[0].libpath(), ['libdir1', 'libdir2'])

        lib_infos = []
        for lib_info in external_library_builders[0].buildinfos():
            if isinstance(lib_info, BuildInfo_Library_External_CMake):
                lib_infos.append(lib_info)
                pass
            pass
        self.failUnlessEqual(len(lib_infos), 1)
        self.failUnlessEqual(lib_infos[0].libs(), ['lib1', 'lib2'])

        macro_infos = []
        for macro_info in external_library_builders[0].buildinfos():
            if isinstance(macro_info, BuildInfo_CommandlineMacros_CMake):
                macro_infos.append(macro_info)
                pass
            pass
        self.failUnlessEqual(len(macro_infos), 1)
        self.failUnlessEqual(macro_infos[0].macros(), {'macro1': 'value1',
                                                       'macro2': 'value2'})

        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(InterfaceInMemorySuite())
    pass

