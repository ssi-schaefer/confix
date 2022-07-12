# Copyright (C) 2010-2013 Joerg Faschingbauer

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

class CustomCommandBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(CustomCommandBuildTest('test_quoting'))
        pass
    pass

class CustomCommandBuildTest(PersistentTestCase):
    def test_quoting(self):
        fs = FileSystem(path=self.rootpath())
        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())
        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())

        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('test_quoting')",
                              "PACKAGE_VERSION('1.2.3')"]))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=[
                    "CMAKE_CMAKELISTS_ADD_CUSTOM_COMMAND__OUTPUT(",
                    "    outputs=['greater_file'],",
                    "    commands=[('touch greater_file > greater_sideeffect', [])],",
                    "    depends=[],",
                    ")",
                    "CMAKE_CMAKELISTS_ADD_CUSTOM_COMMAND__OUTPUT(",
                    "    outputs=['less_file'],",
                    "    commands=[('echo xxx > tmp_file', []),",
                    "              ('cat < tmp_file > less_file', [])],",
                    "    depends=[],",
                    ")",
                    "",
                    "CMAKE_CMAKELISTS_ADD_CUSTOM_TARGET(",
                    "    name='beitl',",
                    "    all=True,",
                    "    depends=['greater_file',",
                    "             'less_file',",
                    "            ]",
                    ")",
                    "",
                    ]))

        package = LocalPackage(rootdirectory=source,
                               setups=[Boilerplate(), CMake(library_dependencies=False)])
        package.boil(external_nodes=[])
        package.output()

        fs.sync()

        commands.cmake(packageroot=source.abspath(), builddir=build.abspath(), args=[])
        commands.make(builddir=build.abspath(), args=[])

        scan.rescan_dir(build)

        self.assertTrue(build.find(['greater_file']))
        self.assertTrue(build.find(['greater_sideeffect']))
        self.assertFalse(build.find(['>']))

        less_file = build.find(['less_file'])
        self.assertTrue(less_file)
        self.assertEqual(len(less_file.lines()), 1)
        self.assertEqual(less_file.lines()[0], 'xxx')

        pass

    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(CustomCommandBuildSuite())
    pass
