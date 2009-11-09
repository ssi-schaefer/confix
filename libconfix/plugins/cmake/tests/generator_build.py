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

from libconfix.testutils.persistent import PersistentTestCase

from libconfix.setups.c import C
from libconfix.setups.cmake import CMake
from libconfix.setups.boilerplate import Boilerplate

from libconfix.core.machinery.local_package import LocalPackage
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
    pass

class GeneratorBuildTest(PersistentTestCase):
    def test_basic(self):
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
                              "    commands=['cp ${PROJECT_SOURCE_DIR}/main.c.template ${PROJECT_BINARY_DIR}/main.c'],",
                              "    depends=['${PROJECT_SOURCE_DIR}/main.c.template'],",
                              "    working_directory=None,",
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

    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(GeneratorBuildSuite())
    pass
