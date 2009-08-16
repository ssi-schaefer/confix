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

class LocalInstallBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(LocalInstallTest('test'))
        pass
    pass

class LocalInstallTest(PersistentTestCase):
    def test(self):
        source = Directory()
        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("intra-package")',
                              'PACKAGE_VERSION("1.2.3")']))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['DIRECTORY(["headers-only"])',
                              'DIRECTORY(["headers-with-library"])',
                              'DIRECTORY(["exe"])']))

        headers_only = source.add(
            name='headers-only',
            entry=Directory())
        headers_with_library = source.add(
            name='headers-with-library',
            entry=Directory())
        exe = source.add(
            name='exe',
            entry=Directory())

        headers_only.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['H(filename="header-1.h", install=["headers-only-install"])',
                              'H(filename="header-2.h", install=["headers-only-install"])']))
        headers_only.add(
            name='header-1.h',
            entry=File())
        headers_only.add(
            name='header-2.h',
            entry=File())

        headers_with_library.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['LIBRARY(members=[H(filename="library-1.h", install=["headers-with-library-install"]),'
                              '                 H(filename="library-2.h", install=["headers-with-library-install"]),'
                              '                 C(filename="library-1.c"),'
                              '                 C(filename="library-2.c")',
                              '                ]',
                              '       )'
                              ]))
        headers_with_library.add(
            name='library-1.h',
            entry=File(lines=['void library1(void);']))
        headers_with_library.add(
            name='library-2.h',
            entry=File(lines=['void library2(void);']))
        headers_with_library.add(
            name='library-1.c',
            entry=File(lines=['#include <headers-only-install/header-1.h>',
                              'void library1(void) {}']))
        headers_with_library.add(
            name='library-2.c',
            entry=File(lines=['#include <headers-only-install/header-2.h>',
                              'void library2(void) {}']))

        exe.add(
            name='main.c',
            entry=File(lines=['#include <headers-only-install/header-1.h>',
                              '#include <headers-only-install/header-2.h>',
                              '#include <headers-with-library-install/library-1.h>',
                              '#include <headers-with-library-install/library-2.h>',
                              'int main(void) {',
                              '    library1();',
                              '    library2();',
                              '}']))

        fs = FileSystem(path=self.rootpath())
        source = fs.rootdirectory().add(
            name='source',
            entry=source)
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

        pass

    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(LocalInstallBuildSuite())
    pass
