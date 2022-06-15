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

from libconfix.plugins.automake import bootstrap
from libconfix.plugins.automake import configure
from libconfix.plugins.automake import make

from libconfix.core.hierarchy.explicit_setup import ExplicitDirectorySetup
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys import scan
from libconfix.core.utils import const
from libconfix.testutils.persistent import PersistentTestCase

from libconfix.setups.c import C
from libconfix.setups.c import AutoC
from libconfix.setups.automake import Automake
from libconfix.setups.boilerplate import Boilerplate

import unittest
import sys

class NoPublicInstall(PersistentTestCase):
    def test__explicit_no_public_visibility(self):
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
            entry=File(lines=["PACKAGE_NAME('blah')",
                              "PACKAGE_VERSION('1.2.3')"]))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["H(filename='header.h', public=False)"]))
        source.add(
            name='header.h',
            entry=File())

        package = LocalPackage(rootdirectory=source,
                               setups=[Boilerplate(),
                                       C(),
                                       Automake(use_libtool=False, library_dependencies=False)])
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
            readonly_prefixes=None)
        make.make(
            builddir=build.abspath(),
            args=['install'])

        scan.rescan_dir(install)

        self.assertFalse(install.find(['include', 'header.h']))
        
        pass
    
    def test__auto_no_public_visibility(self):
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
            entry=File(lines=["PACKAGE_NAME('blah')",
                              "PACKAGE_VERSION('1.2.3')"]))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["SET_HEADER_PUBLIC(shellmatch='header.h', public=False)"]))
        source.add(
            name='header.h',
            entry=File())

        package = LocalPackage(rootdirectory=source,
                               setups=[Boilerplate(),
                                       AutoC(),
                                       Automake(use_libtool=False, library_dependencies=False)])
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
            readonly_prefixes=None)
        make.make(
            builddir=build.abspath(),
            args=['install'])

        scan.rescan_dir(install)

        self.assertFalse(install.find(['include', 'header.h']))

        pass

    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(NoPublicInstall)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
