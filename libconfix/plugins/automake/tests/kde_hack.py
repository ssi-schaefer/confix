# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2008 Joerg Faschingbauer

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

from libconfix.plugins.automake.setup import AutomakeSetup
from libconfix.plugins.automake.kde_hack import KDEHackSetup
from libconfix.plugins.automake.out_automake import AutoconfAuxDirBuilder
from libconfix.plugins.automake import bootstrap, configure, make

from libconfix.core.utils import const
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.hierarchy.implicit_setup import ImplicitDirectorySetup
from libconfix.testutils.persistent import PersistentTestCase

import sys
import unittest

class KDEHackTestSuiteBuild(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(KDEHackTest('test'))
        pass
    pass

class KDEHackTest(PersistentTestCase):
    def test(self):
        fs = FileSystem(path=self.rootpath())

        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())
        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('KDEHackTest')",
                              "PACKAGE_VERSION('1.2.3')"]))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File())

        subdir = source.add(
            name='subdir',
            entry=Directory())
        subdir.add(
            name=const.CONFIX2_DIR,
            entry=File())
        
        
        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())

        package=LocalPackage(rootdirectory=source,
                             setups=[AutomakeSetup(use_libtool=False),
                                     KDEHackSetup(),
                                     ImplicitDirectorySetup()])
        package.boil(external_nodes=[])
        package.output()

        for b in package.rootbuilder().iter_builders():
            if isinstance(b, AutoconfAuxDirBuilder):
                auxdirbuilder = b
                break
            pass
        else:
            self.fail()
            pass

        self.failUnless(source.find([const.ADMIN_DIR, 'automake', 'conf.change.pl']))
        self.failUnless(source.find([const.ADMIN_DIR, 'automake', 'config.pl']))

        fs.sync()

        bootstrap.bootstrap(
            packageroot=source.abspath(),
            path=None,
            use_kde_hack=True,
            argv0=sys.argv[0])
        configure.configure(
            packageroot=source.abspath(),
            builddir=build.abspath(),
            prefix=None,
            readonly_prefixes=None)
        make.make(
            builddir=build.abspath(),
            args=[])
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(KDEHackTestSuiteBuild())
    pass
