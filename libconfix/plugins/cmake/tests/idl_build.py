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

from libconfix.testutils.persistent import PersistentTestCase

from libconfix.plugins.idl.setup import IDLSetup
from libconfix.setups.boilerplate import AutoBoilerplate
from libconfix.setups.cmake import CMake

from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys import scan
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

import unittest
import sys
import os

class IDLBuildTest(PersistentTestCase):

    # we install IDL locally even if this is not absolutely
    # necessary. this makes it easier for real builders (those that
    # wrap IDL compilers) to set the include path.
    def test__localinstall_not_absolutely_necessary(self):
        fs = FileSystem(path=self.rootpath())
        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())
        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())

        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('test_localinstall_not_absolutely_necessary')",
                              "PACKAGE_VERSION('1.2.3')"]))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File())
        source.add(
            name='file.idl',
            entry=File())

        package = LocalPackage(
            rootdirectory=source,
            setups=[AutoBoilerplate(),
                    CMake(library_dependencies=False),
                    IDLSetup()])
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

        scan.rescan_dir(build)

        self.assertTrue(build.find(['confix-include', 'file.idl']))

        pass

    def test__localinstall_necessary(self):
        fs = FileSystem(path=self.rootpath())
        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())
        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())

        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('test_localinstall_necessary')",
                              "PACKAGE_VERSION('1.2.3')"]))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File())
        source.add(
            name='file.idl',
            entry=File(lines=['module A {',
                              'module B {',
                              '}; // /module',
                              '}; // /module',
                              ]))

        package = LocalPackage(
            rootdirectory=source,
            setups=[AutoBoilerplate(),
                    CMake(library_dependencies=False),
                    IDLSetup()])
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

        scan.rescan_dir(build)

        self.assertTrue(build.find(['confix-include', 'A', 'B', 'file.idl']))

        pass

    def test__publicinstall_flat(self):
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
            entry=File(lines=["PACKAGE_NAME('test_publicinstall_flat')",
                              "PACKAGE_VERSION('1.2.3')"]))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File())
        source.add(
            name='file.idl',
            entry=File())

        package = LocalPackage(
            rootdirectory=source,
            setups=[AutoBoilerplate(),
                    CMake(library_dependencies=False),
                    IDLSetup()])
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

        self.assertTrue(install.find(['include', 'file.idl']))

        pass

    def test__publicinstall_subdir(self):
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
            entry=File(lines=["PACKAGE_NAME('test_publicinstall_subdir')",
                              "PACKAGE_VERSION('1.2.3')"]))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File())
        source.add(
            name='file.idl',
            entry=File(lines=['module A {',
                              'module B {',
                              '}; // /module',
                              '}; // /module',
                              ]))

        package = LocalPackage(
            rootdirectory=source,
            setups=[AutoBoilerplate(),
                    CMake(library_dependencies=False),
                    IDLSetup()])
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

        self.assertTrue(install.find(['include', 'A', 'B', 'file.idl']))

        pass

    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(IDLBuildTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
