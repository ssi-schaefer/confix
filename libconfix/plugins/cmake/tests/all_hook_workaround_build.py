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

from libconfix.plugins.cmake import commands

from libconfix.setups.boilerplate import Boilerplate
from libconfix.setups.cmake import CMake

from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys import scan
from libconfix.core.utils import const

from libconfix.testutils.persistent import PersistentTestCase

import unittest

class AllHookWorkaroundBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
#        self.addTest(AllHookWorkaroundBuildTest('test_reproduce'))
        self.addTest(AllHookWorkaroundBuildTest('test_workaround'))
        pass
    pass

class AllHookWorkaroundBuildTest(PersistentTestCase):

    # reproduces cmake bug 0010082. hooking a custom command into the
    # 'all' target twice leads to duplicate execution of the command
    # when doing a parallel build.
    def test_reproduce(self):
        fs = FileSystem(path=self.rootpath())
        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())
        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())

        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('test_reproduce')",
                              "PACKAGE_VERSION('1.2.3')"]))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=[
                'CMAKE_CMAKELISTS_ADD_FIND_CALL(',
                '    find_call=["ADD_CUSTOM_COMMAND(",',
                '               "    OUTPUT generated",',
                '               "    COMMAND sleep 1",',
                '               "    COMMAND echo custom command running",',
                '               "    COMMAND echo I was here >> generated",',
                '               "    COMMAND touch generated",',
                '               ")",',
                '               "ADD_CUSTOM_TARGET(",',
                '               "    my-all-1",',
                '               "    ALL",',
                '               "    DEPENDS generated",',
                '               ")",',
                '               "ADD_CUSTOM_TARGET(",',
                '               "    my-all-2",',
                '               "    ALL",',
                '               "    DEPENDS generated",',
                '               ")",',
                '               ],',
                '    flags=CMAKE_BUILDINFO_LOCAL)',
                ]))

        package = LocalPackage(rootdirectory=source,
                               setups=[Boilerplate(), CMake(library_dependencies=False)])
        package.boil(external_nodes=[])
        package.output()

        fs.sync()

        commands.cmake(packageroot=source.abspath(), builddir=build.abspath(), args=[])
        commands.make(builddir=build.abspath(), args=['-j2'])

        scan.rescan_dir(build)

        self.failUnlessEqual(build.get('generated').lines(), ['I was here', 'I was here'])
        
        pass

    def test_workaround(self):
        fs = FileSystem(path=self.rootpath())
        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())
        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())

        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('test_reproduce')",
                              "PACKAGE_VERSION('1.2.3')"]))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=[
                'from libconfix.plugins.cmake.out_cmake import find_cmake_output_builder',
                'cmake_output_builder = find_cmake_output_builder(CURRENT_BUILDER())',
                'cmake_output_builder.local_cmakelists().add_find_call(',
                '    find_call=["ADD_CUSTOM_COMMAND(",',
                '               "    OUTPUT generated",',
                '               "    COMMAND sleep 1",',
                '               "    COMMAND echo custom command running",',
                '               "    COMMAND echo I was here >> generated",',
                '               "    COMMAND touch generated",',
                '               ")",',
                '               ]),',
                'cmake_output_builder.local_cmakelists().add_all_target_hook(name="my-all-1", depends=["generated"])',
                'cmake_output_builder.local_cmakelists().add_all_target_hook(name="my-all-2", depends=["generated"])',
                ]))

        package = LocalPackage(rootdirectory=source,
                               setups=[Boilerplate(), CMake(library_dependencies=False)])
        package.boil(external_nodes=[])
        package.output()

        fs.sync()

        commands.cmake(packageroot=source.abspath(), builddir=build.abspath(), args=[])
        commands.make(builddir=build.abspath(), args=['-j2'])

        scan.rescan_dir(build)

        self.failUnlessEqual(build.get('generated').lines(), ['I was here'])
        pass

    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(AllHookWorkaroundBuildSuite())
    pass
