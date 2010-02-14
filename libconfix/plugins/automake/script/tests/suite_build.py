# Copyright (C) 2010 Joerg Faschingbauer

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

from libconfix.testutils.persistent import PersistentTestCase

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys import scan
from libconfix.core.utils import const
from libconfix.core.machinery.local_package import LocalPackage

from libconfix.setups.boilerplate import Boilerplate
from libconfix.setups.script import Script
from libconfix.setups.automake import Automake

import stat
import sys
import unittest

class AutomakeScriptBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(AutomakeTestScriptTest('test_true'))
        pass
    pass

class AutomakeTestScriptTest(PersistentTestCase):
    def test_true(self):
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
            entry=File(lines=["PACKAGE_NAME('AutomakeTestScriptTest')",
                              "PACKAGE_VERSION('1.2.3')"]))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=[
                "ADD_SCRIPT(filename='test-true', what=SCRIPT_CHECK)",
                "ADD_SCRIPT(filename='install-dummy', what=SCRIPT_BIN)",
                ]))
        source.add(
            name='test-true',
            entry=File(
                lines=['#!/bin/sh',
                       'touch I-was-here',
                       'exit 0',                
                       ],
                mode=stat.S_IRUSR|stat.S_IXUSR))
        source.add(
            name='install-dummy',
            entry=File(mode=stat.S_IRUSR|stat.S_IXUSR))

        package = LocalPackage(rootdirectory=source,
                               setups=[Boilerplate(),
                                       Script(),
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
            args=['check'])
        make.make(
            builddir=build.abspath(),
            args=['install'])

        # verify that the script was executed.
        scan.rescan_dir(build)
        self.failUnless(build.find(['I-was-here']))

        scan.rescan_dir(install)

        # verify that the script hasn't been installed.
        self.failIf(install.find(['bin', 'I-was-here']))

        # for completeness (and paranoia), check if scripts are
        # installed at all.
        self.failUnless(install.find(['bin', 'install-dummy']))
        
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(AutomakeScriptBuildSuite())
    pass
