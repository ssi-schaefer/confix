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

from libconfix.plugins.cmake import commands
from libconfix.plugins.cmake.out_cmake import find_cmake_output_builder

from libconfix.plugins.c.h import HeaderBuilder

from libconfix.testutils.persistent import PersistentTestCase

from libconfix.setups.c import C
from libconfix.setups.plainfile import Plainfile
from libconfix.setups.cmake import CMake
from libconfix.setups.boilerplate import Boilerplate

from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.machinery.setup import Setup
from libconfix.core.machinery.builder import Builder
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.file import FileState
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys import scan
from libconfix.core.utils import const

import unittest

class GeneratorBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(GeneratorBuildTest('test_basic'))
        self.addTest(GeneratorBuildTest('generated_headers_public_install'))
        self.addTest(GeneratorBuildTest('generated_headers_local_install'))
        self.addTest(GeneratorBuildTest('generated_plainfile_install'))
        self.addTest(GeneratorBuildTest('two_directories_with_generator_same_outputfilename'))
        self.addTest(GeneratorBuildTest('library_depends_on_generated_header__from_a_header_only_directory'))
        pass
    pass

class GeneratorBuildTest(PersistentTestCase):
    def test__basic(self):
        fs = FileSystem(path=self.rootpath())
        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())
        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())

        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('test_basic')",
                              "PACKAGE_VERSION('1.2.3')"]))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["CMAKE_CMAKELISTS_ADD_CUSTOM_COMMAND__OUTPUT(",
                              "    outputs=['main.c'],",
                              "    commands=[('cp', ",
                              "               ['${PROJECT_SOURCE_DIR}/main.c.template', '${PROJECT_BINARY_DIR}/main.c'])],",
                              "    depends=['${PROJECT_SOURCE_DIR}/main.c.template'],",
                              ")",
                              "EXECUTABLE(",
                              "    exename='exe',",
                              "    center=C(filename='main.c')",
                              ")"
                              ]))
        source.add(
            name='main.c.template',
            entry=File(lines=['int main(void) { return 0; }']))
        source.add(
            name='main.c',
            entry=File(state=FileState.VIRTUAL, lines=[]))

        package = LocalPackage(rootdirectory=source,
                               setups=[Boilerplate(), C(), CMake(library_dependencies=False)])
        package.boil(external_nodes=[])
        package.output()

        fs.sync()

        commands.cmake(packageroot=source.abspath(), builddir=build.abspath(), args=[])
        commands.make(builddir=build.abspath(), args=[])

        scan.rescan_dir(build)

        # I doubt that this will hold under Windows :-) if it becomes
        # an issue we will skip this check
        self.failUnless(build.find(['exe']))

        pass

    def test__generated_headers_public_install(self):
        fs = FileSystem(path=self.rootpath())
        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())
        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())
        install = fs.rootdirectory().add(
            name='install',
            entry=Directory())

        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('generated_headers_public_install')",
                              "PACKAGE_VERSION('1.2.3')"]))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=[
                "LIBRARY(members=[H(filename='generated.h'), C(filename='generated.c')])",
                "CMAKE_CMAKELISTS_ADD_CUSTOM_COMMAND__OUTPUT(",
                "    outputs=['generated.h', 'generated.c'],",
                "    commands=[('touch', ['generated.h']),",
                "              ('touch', ['generated.c'])],",
                "    depends=[],",
                ")",
                ]))
        source.add(
            name='generated.h',
            entry=File(state=FileState.VIRTUAL, lines=[]))
        source.add(
            name='generated.c',
            entry=File(state=FileState.VIRTUAL, lines=[]))

        package = LocalPackage(rootdirectory=source,
                               setups=[Boilerplate(), C(), CMake(library_dependencies=False)])
        package.boil(external_nodes=[])
        package.output()

        fs.sync()

        commands.cmake(
            packageroot=source.abspath(),
            builddir=build.abspath(),
            args=['-DCMAKE_INSTALL_PREFIX='+'/'.join(install.abspath())])
        commands.make(
            builddir=build.abspath(),
            args=['install'])

        scan.rescan_dir(install)

        self.failUnless(install.find(['include', 'generated.h']))

        pass

    def test__generated_headers_local_install(self):
        fs = FileSystem(path=self.rootpath())
        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())
        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())
        install = fs.rootdirectory().add(
            name='install',
            entry=Directory())

        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('generated_headers_local_install')",
                              "PACKAGE_VERSION('1.2.3')"]))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["DIRECTORY(['generated'])",
                              "DIRECTORY(['exe'])"]))
        
        generated = source.add(
            name='generated',
            entry=Directory())

        generated.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=[
                "LIBRARY(members=[H(filename='generated.h', install=['a']), C(filename='generated.c')])",
                "CMAKE_CMAKELISTS_ADD_CUSTOM_COMMAND__OUTPUT(",
                "    outputs=['generated.h', 'generated.c'],",
                "    commands=[('touch', ['generated.h']),",
                "              ('touch', ['generated.c'])],",
                "    depends=[],",
                ")",
                ]))
        generated.add(
            name='generated.h',
            entry=File(state=FileState.VIRTUAL, lines=[]))
        generated.add(
            name='generated.c',
            entry=File(state=FileState.VIRTUAL, lines=[]))

        exe = source.add(
            name='exe',
            entry=Directory())
        exe.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["EXECUTABLE(center=C(filename='main.c'))"]))
        exe.add(
            name='main.c',
            entry=File(lines=[
                '#include <a/generated.h>',
                'int main(void) {}',
                ]))

        package = LocalPackage(rootdirectory=source,
                               setups=[Boilerplate(), C(), CMake(library_dependencies=False)])
        package.boil(external_nodes=[])
        package.output()

        fs.sync()

        commands.cmake(
            packageroot=source.abspath(),
            builddir=build.abspath(),
            args=['-DCMAKE_INSTALL_PREFIX='+'/'.join(install.abspath())])
        commands.make(
            builddir=build.abspath(),
            args=['install'])

        scan.rescan_dir(install)
        scan.rescan_dir(build)

        self.failUnless(install.find(['include', 'a', 'generated.h']))

        pass

    def test__generated_plainfile_install(self):
        fs = FileSystem(path=self.rootpath())
        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())
        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())
        install = fs.rootdirectory().add(
            name='install',
            entry=Directory())

        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('generated_plainfile_install')",
                              "PACKAGE_VERSION('1.2.3')"]))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=[
                "ADD_PLAINFILE(filename='prefixfile', prefixdir='prefixdir')",
                "ADD_PLAINFILE(filename='datafile', datadir='datadir')",
                "CMAKE_CMAKELISTS_ADD_CUSTOM_COMMAND__OUTPUT(",
                "    outputs=['prefixfile', 'datafile'],",
                "    commands=[('touch', ['prefixfile']),",
                "              ('touch', ['datafile'])],",
                "    depends=[],",
                ")",
                # without doing anything, nothing will be built. hook
                # it to the 'all' target.
                "CMAKE_CMAKELISTS_ADD_CUSTOM_TARGET(",
                "    name='generate_those_bloody_files_when_I_say_make',",
                "    all=True,",
                "    depends=['prefixfile', 'datafile'],",
                ")",
                ]))
        source.add(
            name='prefixfile',
            entry=File(state=FileState.VIRTUAL, lines=[]))
        source.add(
            name='datafile',
            entry=File(state=FileState.VIRTUAL, lines=[]))

        package = LocalPackage(rootdirectory=source,
                               setups=[Boilerplate(), Plainfile(), CMake(library_dependencies=False)])
        package.boil(external_nodes=[])
        package.output()

        fs.sync()

        commands.cmake(
            packageroot=source.abspath(),
            builddir=build.abspath(),
            args=['-DCMAKE_INSTALL_PREFIX='+'/'.join(install.abspath())])
        commands.make(
            builddir=build.abspath(),
            args=['install'])

        scan.rescan_dir(install)

        self.failUnless(install.find(['prefixdir', 'prefixfile']))
        self.failUnless(install.find(['share', 'datadir', 'datafile']))

        pass
    
    def two_directories_with_generator_same_outputfilename(self):
        """
        The artificial custom target that we generate for every custom
        command has a name that is derived from the command's
        output(s). This leads to clashes when two directories have
        commands that generate outputs with the same name.
        """

        fs = FileSystem(path=self.rootpath())
        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())
        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())

        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('two_directories_with_generator_same_outputfilename')",
                              "PACKAGE_VERSION('1.2.3')"]))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['DIRECTORY(["dira"])',
                              'DIRECTORY(["dirb"])']))

        dira = source.add(
            name='dira',
            entry=Directory())
        dira.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['CMAKE_CMAKELISTS_ADD_CUSTOM_COMMAND__OUTPUT(',
                              '    outputs=["output"],',
                              '    commands=[("touch", ["output"])],',
                              '    depends=[])']))

        dirb = source.add(
            name='dirb',
            entry=Directory())
        dirb.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['CMAKE_CMAKELISTS_ADD_CUSTOM_COMMAND__OUTPUT(',
                              '    outputs=["output"],',
                              '    commands=[("touch", ["output"])],',
                              '    depends=[])']))

        package = LocalPackage(rootdirectory=source,
                               setups=[Boilerplate(), Plainfile(), CMake(library_dependencies=False)])
        package.boil(external_nodes=[])
        package.output()

        fs.sync()

        commands.cmake(
            packageroot=source.abspath(),
            builddir=build.abspath(),
            args=[])
        commands.make(
            builddir=build.abspath(),
            args=[])

        pass

    def library_depends_on_generated_header__from_a_header_only_directory(self):
        fs = FileSystem(path=self.rootpath())
        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())
        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())

        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('library_depends_on_generated_header__from_a_header_only_directory')",
                              "PACKAGE_VERSION('1.2.3')"]))
        generated_header = source.add(
            name='generated-header',
            entry=Directory())

        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["DIRECTORY(['generated-header'])",
                              "DIRECTORY(['library1'])",
                              "DIRECTORY(['library2'])",
                              ]))

        library1 = source.add(
            name='library1',
            entry=Directory())
        library1.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["LIBRARY(members=[C(filename='using-generated-header.c')])"]))
        library1.add(
            name='using-generated-header.c',
            entry=File(lines=['#include <generated-header.h>']))

        library2 = source.add(
            name='library2',
            entry=Directory())
        library2.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["LIBRARY(members=[C(filename='using-generated-header.c')])"]))
        library2.add(
            name='using-generated-header.c',
            entry=File(lines=['#include <generated-header.h>']))

        package = LocalPackage(rootdirectory=source,
                               setups=[Boilerplate(), C(), CMake(library_dependencies=False),
                                       GeneratedHeaderSetup()])
        package.boil(external_nodes=[])
        package.output()

        fs.sync()

        commands.cmake(
            packageroot=source.abspath(),
            builddir=build.abspath())
        commands.make(
            builddir=build.abspath(),
            args=['-j', 'VERBOSE=1'])
        pass

    pass

class GeneratedHeaderSetup(Setup):
    def setup(self, dirbuilder):
        if dirbuilder.directory().name() == 'generated-header':
            dirbuilder.add_builder(HeaderGenerator())
            pass
        pass
    pass
        
class HeaderGenerator(Builder):
    def __init__(self):
        Builder.__init__(self)
        self.__exploded = False
        pass
    def locally_unique_id(self):
        return str(self.__class__)
    def enlarge(self):
        super(HeaderGenerator, self).enlarge()
        if self.__exploded:
            return
        self.__exploded = True
        generated_header = self.parentbuilder().directory().add(
            name='generated-header.h',
            entry=File(state=FileState.VIRTUAL, lines=[]))
        self.parentbuilder().add_builder(HeaderBuilder(file=generated_header))
        pass
    def output(self):
        super(HeaderGenerator, self).output()
        cmake_output = find_cmake_output_builder(self.parentbuilder())
        cmake_output.local_cmakelists().add_custom_command__output(
            outputs=['generated-header.h'],
            commands=[('echo', ['generating generated-header.h']), ('touch', ['generated-header.h'])],
            depends=[])
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
