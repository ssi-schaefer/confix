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
from libconfix.plugins.cmake.buildinfo import BuildInfo_IncludePath_External_CMake
from libconfix.plugins.cmake.buildinfo import BuildInfo_LibraryPath_External_CMake
from libconfix.plugins.cmake.buildinfo import BuildInfo_Toplevel_CMakeLists_Include
from libconfix.plugins.cmake.buildinfo import BuildInfo_Toplevel_CMakeLists_FindCall
from libconfix.plugins.cmake.buildinfo import BuildInfo_Library_External_CMake
from libconfix.plugins.cmake.buildinfo import BuildInfo_CommandlineMacros_CMake

from libconfix.setups.boilerplate import Boilerplate
from libconfix.setups.cmake import CMake
from libconfix.setups.c import C

from libconfix.plugins.c.setups.explicit_setup import ExplicitCSetup

from libconfix.core.hierarchy.explicit_setup import ExplicitDirectorySetup
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.utils import const

import itertools
import unittest

class InterfaceInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(InterfaceInMemoryTest('test_CMAKE_ADD_MODULE_FILE'))

        self.addTest(InterfaceInMemoryTest('test_CMAKE_CMAKELISTS_ADD_INCLUDE_local_only'))
        self.addTest(InterfaceInMemoryTest('test_CMAKE_CMAKELISTS_ADD_INCLUDE_propagate_only'))
        self.addTest(InterfaceInMemoryTest('test_CMAKE_CMAKELISTS_ADD_INCLUDE_propagate_and_local'))
        self.addTest(InterfaceInMemoryTest('test_CMAKE_CMAKELISTS_ADD_INCLUDE_DIRECTORY_local'))
        self.addTest(InterfaceInMemoryTest('test_CMAKE_CMAKELISTS_ADD_INCLUDE_DIRECTORY_propagate'))
        self.addTest(InterfaceInMemoryTest('test_CMAKE_CMAKELISTS_ADD_FIND_CALL_local_only'))
        self.addTest(InterfaceInMemoryTest('test_CMAKE_CMAKELISTS_ADD_FIND_CALL_propagate_only'))
        self.addTest(InterfaceInMemoryTest('test_CMAKE_CMAKELISTS_ADD_FIND_CALL_propagate_and_local'))
        self.addTest(InterfaceInMemoryTest('test_CMAKE_CMAKELISTS_ADD_FIND_CALL_multiline'))

        self.addTest(InterfaceInMemoryTest('test_CMAKE_CMDLINE_MACROS_local_only'))
        self.addTest(InterfaceInMemoryTest('test_CMAKE_CMDLINE_MACROS_propagate_only'))
        self.addTest(InterfaceInMemoryTest('test_CMAKE_CMDLINE_MACROS_propagate_and_local'))
        self.addTest(InterfaceInMemoryTest('test_CMAKE_EXTERNAL_LIBRARY'))
        self.addTest(InterfaceInMemoryTest('test_CMAKE_PKG_CONFIG_LIBRARY'))
        pass
    pass

class InterfaceInMemoryTest(unittest.TestCase):
    def test_CMAKE_ADD_MODULE_FILE(self):
        fs = FileSystem(path=[''])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("test_CMAKE_ADD_MODULE_FILE")',
                              'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['CMAKE_ADD_MODULE_FILE(',
                              '    name="file1",',
                              '    lines=["xxx"],'
                              '    flags=CMAKE_BUILDINFO_LOCAL)',
                              'CMAKE_ADD_MODULE_FILE(',
                              '    name="file2",',
                              '    lines=["xxx"],',
                              '    flags=CMAKE_BUILDINFO_LOCAL)']))

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

        for buildinfo in package.rootbuilder().iter_buildinfos():
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

        for buildinfo in package.rootbuilder().iter_buildinfos():
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

        for buildinfo in package.rootbuilder().iter_buildinfos():
            if isinstance(buildinfo, BuildInfo_Toplevel_CMakeLists_Include):
                break
            pass
        else:
            self.fail()
            pass
        pass

    def test_CMAKE_CMAKELISTS_ADD_INCLUDE_DIRECTORY_local(self):
        fs = FileSystem(path=[''])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("test_CMAKE_CMAKELISTS_ADD_INCLUDE_DIRECTORY_local")',
                              'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['DIRECTORY(["subdir"])']))

        subdir = fs.rootdirectory().add(
            name='subdir',
            entry=Directory())
        subdir.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['CMAKE_CMAKELISTS_ADD_INCLUDE_DIRECTORY("include-directory", CMAKE_BUILDINFO_LOCAL)']))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitDirectorySetup(), CMakeSetup()])
        package.boil(external_nodes=[])
        package.output()

        cmake_output_builder = find_cmake_output_builder(package.rootbuilder().find_entry_builder(['subdir']))
        self.failUnless('include-directory' in cmake_output_builder.local_cmakelists().get_include_directories())
        pass

    def test_CMAKE_CMAKELISTS_ADD_INCLUDE_DIRECTORY_propagate(self):
        fs = FileSystem(path=[''])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("test_CMAKE_CMAKELISTS_ADD_INCLUDE_DIRECTORY_propagate")',
                              'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['DIRECTORY(["sender"])',
                              'DIRECTORY(["receiver"])']))

        sender = fs.rootdirectory().add(
            name='sender',
            entry=Directory())
        sender.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['PROVIDE_SYMBOL("sender")',
                              'CMAKE_CMAKELISTS_ADD_INCLUDE_DIRECTORY("include-directory", CMAKE_BUILDINFO_PROPAGATE)']))

        receiver = fs.rootdirectory().add(
            name='receiver',
            entry=Directory())
        receiver.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['REQUIRE_SYMBOL("sender", URGENCY_ERROR)',
                              'C(filename="file.c")']))
        # need a compiled file builder in order for the include path
        # to show up in the CMakeLists.txt.
        receiver.add(
            name='file.c',
            entry=File())

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[Boilerplate(), C(), CMake(library_dependencies=False)])
        package.boil(external_nodes=[])
        package.output()

        cmake_output_builder = find_cmake_output_builder(package.rootbuilder().find_entry_builder(['receiver']))
        self.failUnless('include-directory' in cmake_output_builder.local_cmakelists().get_include_directories())
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

        for buildinfo in package.rootbuilder().iter_buildinfos():
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

        for buildinfo in package.rootbuilder().iter_buildinfos():
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

        for buildinfo in package.rootbuilder().iter_buildinfos():
            if isinstance(buildinfo, BuildInfo_Toplevel_CMakeLists_FindCall):
                break
            pass
        else:
            self.fail()
            pass
        pass

    def test_CMAKE_CMAKELISTS_ADD_FIND_CALL_multiline(self):
        fs = FileSystem(path=[''])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("test_CMAKE_CMAKELISTS_ADD_FIND_CALL_multiline")',
                              'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['CMAKE_CMAKELISTS_ADD_FIND_CALL(["call1", "call2"], CMAKE_BUILDINFO_LOCAL)']))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitDirectorySetup(), CMakeSetup()])
        package.boil(external_nodes=[])
        package.output()

        self.failUnless('call1' in find_cmake_output_builder(package.rootbuilder()).top_cmakelists().get_find_calls())
        self.failUnless('call2' in find_cmake_output_builder(package.rootbuilder()).top_cmakelists().get_find_calls())

        for buildinfo in package.rootbuilder().iter_buildinfos():
            self.failIf(isinstance(buildinfo, BuildInfo_Toplevel_CMakeLists_FindCall))
            pass
        pass

    def test_CMAKE_CMDLINE_MACROS_local_only(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("test_CMAKE_CMDLINE_MACROS_local_only")',
                              'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['CMAKE_CMDLINE_MACROS(macros={"macro1": "value1", "macro2": "value2"}, flags=CMAKE_BUILDINFO_LOCAL)']))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitDirectorySetup(), CMakeSetup()])
        package.boil(external_nodes=[])
        package.output()

        self.failUnless("-Dmacro1=value1" in find_cmake_output_builder(package.rootbuilder()).local_cmakelists().get_definitions())
        self.failUnless("-Dmacro2=value2" in find_cmake_output_builder(package.rootbuilder()).local_cmakelists().get_definitions())

        for buildinfo in package.rootbuilder().iter_buildinfos():
            self.failIf(isinstance(buildinfo, BuildInfo_CommandlineMacros_CMake))
            pass
        pass

    def test_CMAKE_CMDLINE_MACROS_propagate_only(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("test_CMAKE_CMDLINE_MACROS_propagate_only")',
                              'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['CMAKE_CMDLINE_MACROS(macros={"macro1": "value1", "macro2": "value2"}, flags=CMAKE_BUILDINFO_PROPAGATE)']))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitDirectorySetup(), CMakeSetup()])
        package.boil(external_nodes=[])
        package.output()

        self.failIf("-Dmacro1=value1" in find_cmake_output_builder(package.rootbuilder()).local_cmakelists().get_definitions())
        self.failIf("-Dmacro2=value2" in find_cmake_output_builder(package.rootbuilder()).local_cmakelists().get_definitions())

        for buildinfo in package.rootbuilder().iter_buildinfos():
            if isinstance(buildinfo, BuildInfo_CommandlineMacros_CMake):
                self.failUnlessEqual(buildinfo.macros().get('macro1'), 'value1')
                self.failUnlessEqual(buildinfo.macros().get('macro2'), 'value2')
                break
            pass
        else:
            self.fail()
            pass
        pass

    def test_CMAKE_CMDLINE_MACROS_propagate_and_local(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("test_CMAKE_CMDLINE_MACROS_propagate_and_local")',
                              'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['CMAKE_CMDLINE_MACROS(macros={"macro1": "value1", "macro2": "value2"}, flags=CMAKE_BUILDINFO_PROPAGATE)']))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitDirectorySetup(), CMakeSetup()])
        package.boil(external_nodes=[])
        package.output()

        self.failIf("-Dmacro1=value1" in find_cmake_output_builder(package.rootbuilder()).local_cmakelists().get_definitions())
        self.failIf("-Dmacro2=value2" in find_cmake_output_builder(package.rootbuilder()).local_cmakelists().get_definitions())

        for buildinfo in package.rootbuilder().iter_buildinfos():
            if isinstance(buildinfo, BuildInfo_CommandlineMacros_CMake):
                self.failUnlessEqual(buildinfo.macros().get('macro1'), 'value1')
                self.failUnlessEqual(buildinfo.macros().get('macro2'), 'value2')
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
        for incpath_info in external_library_builders[0].iter_buildinfos():
            if isinstance(incpath_info, BuildInfo_IncludePath_External_CMake):
                incpath_infos.append(incpath_info)
                pass
            pass
        self.failUnlessEqual(len(incpath_infos), 1)
        self.failUnlessEqual(incpath_infos[0].incpath(), ['includedir1', 'includedir2'])

        libpath_infos = []
        for libpath_info in external_library_builders[0].iter_buildinfos():
            if isinstance(libpath_info, BuildInfo_LibraryPath_External_CMake):
                libpath_infos.append(libpath_info)
                pass
            pass
        self.failUnlessEqual(len(libpath_infos), 1)
        self.failUnlessEqual(libpath_infos[0].libpath(), ['libdir1', 'libdir2'])

        lib_infos = []
        for lib_info in external_library_builders[0].iter_buildinfos():
            if isinstance(lib_info, BuildInfo_Library_External_CMake):
                lib_infos.append(lib_info)
                pass
            pass
        self.failUnlessEqual(len(lib_infos), 1)
        self.failUnlessEqual(lib_infos[0].libs(), ['lib1', 'lib2'])

        macro_infos = []
        for macro_info in external_library_builders[0].iter_buildinfos():
            if isinstance(macro_info, BuildInfo_CommandlineMacros_CMake):
                macro_infos.append(macro_info)
                pass
            pass
        self.failUnlessEqual(len(macro_infos), 1)
        self.failUnlessEqual(macro_infos[0].macros(), {'macro1': 'value1',
                                                       'macro2': 'value2'})

        pass

    def test_CMAKE_PKG_CONFIG_LIBRARY(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('test_CMAKE_PKG_CONFIG_LIBRARY')",
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
            entry=File(lines=["PROVIDE_SYMBOL('xxx-glue')",
                              "CMAKE_PKG_CONFIG_LIBRARY(packagename='xxx')"]))
        
        linked = fs.rootdirectory().add(
            name='linked',
            entry=Directory())
        linked.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["REQUIRE_SYMBOL('xxx-glue', URGENCY_ERROR)",
                              "EXECUTABLE(exename='exe', center=C(filename='main.c'))"]))
        linked.add(
            name='main.c',
            entry=File(lines=['int main(void() {}']))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitDirectorySetup(), CMakeSetup(), ExplicitCSetup()])
        package.boil(external_nodes=[])
        package.output()

        linked_cmake_output_builder = find_cmake_output_builder(package.rootbuilder().find_entry_builder(['linked']))

        self.failUnless('FIND_PACKAGE(PkgConfig)' in linked_cmake_output_builder.top_cmakelists().get_find_calls())
        self.failUnless('PKG_CHECK_MODULES(CONFIX_CMAKE_PKG_CONFIG__xxx REQUIRED xxx)' in
                        linked_cmake_output_builder.top_cmakelists().get_find_calls())

        self.failUnless('${CONFIX_CMAKE_PKG_CONFIG__xxx_LIBRARIES}' in
                        linked_cmake_output_builder.local_cmakelists().get_target_link_libraries('exe'))
        self.failUnless('${CONFIX_CMAKE_PKG_CONFIG__xxx_LIBRARY_DIRS}' in
                        linked_cmake_output_builder.local_cmakelists().get_link_directories())
        self.failUnless('${CONFIX_CMAKE_PKG_CONFIG__xxx_INCLUDE_DIRS}' in
                        linked_cmake_output_builder.local_cmakelists().get_include_directories())
        self.failUnless('${CONFIX_CMAKE_PKG_CONFIG__xxx_CFLAGS}' in
                        linked_cmake_output_builder.local_cmakelists().get_definitions())
        self.failUnless('${CONFIX_CMAKE_PKG_CONFIG__xxx_CFLAGS_OTHER}' in
                        linked_cmake_output_builder.local_cmakelists().get_definitions())

        pass

    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(InterfaceInMemorySuite())
    pass

