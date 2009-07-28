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
from libconfix.plugins.cmake import commands

from libconfix.plugins.c.setups.explicit_setup import ExplicitCSetup

from libconfix.core.hierarchy.explicit_setup import ExplicitDirectorySetup
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys import scan
from libconfix.core.utils import const
from libconfix.testutils.persistent import PersistentTestCase

import unittest

class LibraryBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(LibraryTest('single_library'))
        pass
    pass

class LibraryTest(PersistentTestCase):
    def single_library(self):
        fs = FileSystem(path=self.rootpath())
        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())
        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("LibraryTest.basic_test")',
                              'PACKAGE_VERSION("1.2.3")']))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['LIBRARY(basename="the-library",',
                              '        members=[C(filename="file.c"),',
                              '                 H(filename="file.h")])']))
        source.add(
            name='file.h',
            entry=File())
        source.add(
            name='file.c',
            entry=File())

        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())

        package = LocalPackage(rootdirectory=source,
                               setups=[ExplicitDirectorySetup(), ExplicitCSetup(), CMakeSetup()])
        package.boil(external_nodes=[])
        package.output()

        fs.sync()

        commands.cmake(packageroot=source.abspath(), builddir=build.abspath())
        commands.make(builddir=build.abspath(), args=[])

        scan.rescan_dir(build)

        # I don't know if this will hold under Windows :-)
        self.failUnless(build.get('libthe-library.a'))

        pass

    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(LibraryBuildSuite())
    pass
