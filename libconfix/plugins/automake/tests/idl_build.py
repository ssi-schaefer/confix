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

from libconfix.testutils.persistent import PersistentTestCase

from libconfix.plugins.automake import bootstrap
from libconfix.plugins.automake import configure
from libconfix.plugins.automake import make
from libconfix.plugins.idl.setup import IDLSetup
from libconfix.setups.boilerplate import AutoBoilerplate
from libconfix.setups.automake import Automake

from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys import scan
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

import unittest
import sys
import os

class AutomakeIDLBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(AutomakeIDLBuildTest('test_localinstall_not_absolutely_necessary'))
        self.addTest(AutomakeIDLBuildTest('test_localinstall_necessary'))
        self.addTest(AutomakeIDLBuildTest('test_publicinstall_flat'))
        self.addTest(AutomakeIDLBuildTest('test_publicinstall_subdir'))
        pass
    pass

class AutomakeIDLBuildTest(PersistentTestCase):

    # we install IDL locally even if this is not absolutely
    # necessary. this makes it easier for real builders (those that
    # wrap IDL compilers) to set the include path.
    def test_localinstall_not_absolutely_necessary(self):
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
                    Automake(use_libtool=False, library_dependencies=False),
                    IDLSetup()])
        package.boil(external_nodes=[])
        package.output()
        fs.sync()

        bootstrap.bootstrap(
            packageroot=source.abspath(),
            path=None,
            use_kde_hack=False,
            argv0=sys.argv[0])
        configure.configure(
            packageroot=source.abspath(),
            builddir=build.abspath(),
            prefix='/dev/null'.split(os.sep),
            readonly_prefixes=[])
        make.make(
            builddir=build.abspath(),
            args=[])

        scan.rescan_dir(build)

        self.failUnless(build.find(['confix-include', 'file.idl']))

        pass

    def test_localinstall_necessary(self):
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
                    Automake(use_libtool=False, library_dependencies=False),
                    IDLSetup()])
        package.boil(external_nodes=[])
        package.output()
        fs.sync()

        bootstrap.bootstrap(
            packageroot=source.abspath(),
            path=None,
            use_kde_hack=False,
            argv0=sys.argv[0])
        configure.configure(
            packageroot=source.abspath(),
            builddir=build.abspath(),
            prefix='/dev/null'.split(os.sep),
            readonly_prefixes=[])
        make.make(
            builddir=build.abspath(),
            args=[])

        scan.rescan_dir(build)

        self.failUnless(build.find(['confix-include', 'A', 'B', 'file.idl']))

        pass

    def test_publicinstall_flat(self):
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
                    Automake(use_libtool=False, library_dependencies=False),
                    IDLSetup()])
        package.boil(external_nodes=[])
        package.output()
        fs.sync()

        bootstrap.bootstrap(
            packageroot=source.abspath(),
            path=None,
            use_kde_hack=False,
            argv0=sys.argv[0])
        configure.configure(
            packageroot=source.abspath(),
            builddir=build.abspath(),
            prefix=install.abspath(),
            readonly_prefixes=[])
        make.make(
            builddir=build.abspath(),
            args=['install'])

        scan.rescan_dir(install)

        self.failUnless(install.find(['include', 'file.idl']))

        pass

    def test_publicinstall_subdir(self):
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
                    Automake(use_libtool=False, library_dependencies=False),
                    IDLSetup()])
        package.boil(external_nodes=[])
        package.output()
        fs.sync()

        bootstrap.bootstrap(
            packageroot=source.abspath(),
            path=None,
            use_kde_hack=False,
            argv0=sys.argv[0])
        configure.configure(
            packageroot=source.abspath(),
            builddir=build.abspath(),
            prefix=install.abspath(),
            readonly_prefixes=[])
        make.make(
            builddir=build.abspath(),
            args=['install'])

        scan.rescan_dir(install)

        self.failUnless(install.find(['include', 'A', 'B', 'file.idl']))

        pass

    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(AutomakeIDLBuildSuite())
    pass
