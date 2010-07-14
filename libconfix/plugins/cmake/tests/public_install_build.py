# Copyright (C) 2009-2010 Joerg Faschingbauer

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

import os
import unittest

class PublicInstallBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(PublicInstallTest('test'))
        pass
    pass

class PublicInstallTest(PersistentTestCase):
    def test(self):
        source = Directory()
        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("Public-Install")',
                              'PACKAGE_VERSION("1.2.3")']))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['DIRECTORY(["headers"])',
                              'DIRECTORY(["library"])',
                              'DIRECTORY(["exe"])',
                              'DIRECTORY(["test"])']))

        headers = source.add(
            name='headers',
            entry=Directory())
        library = source.add(
            name='library',
            entry=Directory())
        exe = source.add(
            name='exe',
            entry=Directory())
        test = source.add(
            name='test',
            entry=Directory())

        headers.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['H(filename="flat-header.h")',
                              'H(filename="subdir-header.h", install=["subdir"])',
                              ]))
        headers.add(
            name='flat-header.h',
            entry=File())
        headers.add(
            name='subdir-header.h',
            entry=File())

        library.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['LIBRARY(basename="rary", members=[C(filename="library.c")])']))
        library.add(
            name='library.c',
            entry=File())

        exe.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['EXECUTABLE(exename="exe",',
                              '           center=C(filename="main.c"))',
                              ]))
        exe.add(
            name='main.c',
            entry=File(lines=['int main(void) { return 0; }']))

        test.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['EXECUTABLE(exename="test",',
                              '           center=C(filename="main.c"),',
                              '           what=EXECUTABLE_CHECK)',
                              ]))
        test.add(
            name='main.c',
            entry=File(lines=['int main(void) { return 0; }']))

        fs = FileSystem(path=self.rootpath())
        source = fs.rootdirectory().add(
            name='source',
            entry=source)
        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())
        install = fs.rootdirectory().add(
            name='install',
            entry=Directory())

        package = LocalPackage(rootdirectory=source,
                               setups=[ExplicitDirectorySetup(), ExplicitCSetup(), CMakeSetup()])
        package.boil(external_nodes=[])
        package.output()

        fs.sync()

        commands.cmake(
            packageroot=source.abspath(),
            builddir=build.abspath(),
            args=['-DCMAKE_INSTALL_PREFIX='+os.sep.join(install.abspath())])
        commands.make(
            builddir=build.abspath(),
            args=['install'])

        scan.rescan_dir(install)

        self.failUnless(install.find(['include', 'flat-header.h']))
        self.failUnless(install.find(['include', 'subdir', 'subdir-header.h']))

        # if this fails, then you probably are running on Windows.
        self.failUnless(install.find(['lib', 'library.a']))
        self.failUnless(install.find(['bin', 'exe']))
        self.failIf(install.find(['bin', 'test']))

        self.failUnless(install.find(['share', 'confix-%s' % const.REPO_VERSION, 'repo', package.repofilename()]))
        
        pass

    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(PublicInstallBuildSuite())
    pass
