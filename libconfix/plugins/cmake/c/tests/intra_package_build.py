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

class IntraPackageBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(IntraPackageTest('libraries_with_native_local_dependencies'))
        pass
    pass

class IntraPackageTest(PersistentTestCase):
    def libraries_with_native_local_dependencies(self):
        fs = FileSystem(path=self.rootpath())
        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())
        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())
        
        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("LibraryTest.basic_test")',
                              'PACKAGE_VERSION("1.2.3")']))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['DIRECTORY(["lo"])',
                              'DIRECTORY(["hi"])',
                              'DIRECTORY(["hiest"])']))
        lo = source.add(
            name='lo',
            entry=Directory())
        lo.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['LIBRARY(basename="lo",',
                              '        members=[C(filename="lo.c"),',
                              '                 H(filename="lo.h")])']))
        lo.add(
            name='lo.h',
            entry=File())
        lo.add(
            name='lo.c',
            entry=File())
        
        hi = source.add(
            name='hi',
            entry=Directory())
        hi.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['LIBRARY(basename="hi",',
                              '        members=[C(filename="hi.c"),',
                              '                 H(filename="hi.h")])']))
        hi.add(
            name='hi.h',
            entry=File())
        hi.add(
            name='hi.c',
            entry=File(lines=['#include <lo.h>']))

        hiest = source.add(
            name='hiest',
            entry=Directory())
        hiest.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['LIBRARY(basename="hiest",',
                              '        members=[C(filename="hiest.c"),',
                              '                 H(filename="hiest.h")])']))
        hiest.add(
            name='hiest.h',
            entry=File())
        hiest.add(
            name='hiest.c',
            entry=File(lines=['#include <hi.h>']))

        package = LocalPackage(rootdirectory=source,
                               setups=[ExplicitDirectorySetup(), ExplicitCSetup(), CMakeSetup()])
        package.boil(external_nodes=[])
        package.output()

        fs.sync()

        commands.cmake(packageroot=source.abspath(), builddir=build.abspath())
        commands.make(builddir=build.abspath(), args=[])

        scan.rescan_dir(build)

        # I don't know if this will hold under Windows. if it becomes
        # an issue we will skip this check
        self.failUnless(build.find(['lo', 'liblo.a']))
        self.failUnless(build.find(['hi', 'libhi.a']))
        self.failUnless(build.find(['hiest', 'libhiest.a']))

        pass

    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(IntraPackageBuildSuite())
    pass
