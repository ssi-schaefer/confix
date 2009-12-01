# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2009 Joerg Faschingbauer

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

from libconfix.plugins.automake.out_automake import find_automake_output_builder

from libconfix.plugins.plainfile.builder import PlainFileBuilder
from libconfix.plugins.plainfile.setup import PlainFileInterfaceSetup

from libconfix.testutils.persistent import PersistentTestCase

from libconfix.plugins.automake.setup import AutomakeSetup
from libconfix.plugins.automake import bootstrap, configure, make

from libconfix.setups.plainfile import Plainfile
from libconfix.setups.automake import Automake 
from libconfix.setups.boilerplate import Boilerplate 

from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.hierarchy.implicit_setup import ImplicitDirectorySetup
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

import os
import sys
import unittest

class AutomakePlainfileBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(AutomakePlainfileBuildTest('test'))
        pass
    pass

class AutomakePlainfileBuildTest(PersistentTestCase):
    def __init__(self, methodname):
        PersistentTestCase.__init__(self, methodname)
        pass

    def test(self):
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
            entry=File(lines=["PACKAGE_NAME('SimplePlainFileTest')",
                              "PACKAGE_VERSION('1.2.3')"]))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["ADD_PLAINFILE(filename='plainfile_data', ",
                              "              datadir=['subdir', 'data'])", # list of path components
                              "ADD_PLAINFILE(filename='plainfile_prefix',",
                              "              prefixdir='subdir/prefix')", # string
                              ]))
        source.add(
            name='plainfile_data',
            entry=File())
        source.add(
            name='plainfile_prefix',
            entry=File())

        package = LocalPackage(rootdirectory=source,
                               setups=[Boilerplate(), Plainfile(), Automake(use_libtool=False, library_dependencies=False)])
        package.boil(external_nodes=[])
        package.output()

        automake_output_builder = find_automake_output_builder(package.rootbuilder())
        self.failUnless('plainfile_data' in automake_output_builder.makefile_am().extra_dist())
        self.failUnless('plainfile_prefix' in automake_output_builder.makefile_am().extra_dist())
        
        fs.sync()

        bootstrap.bootstrap(
            packageroot=source.abspath(),
            path=None,
            use_kde_hack=False, # (same)
            argv0=sys.argv[0])
        configure.configure(
            packageroot=source.abspath(),
            builddir=build.abspath(),
            prefix=install.abspath(),
            readonly_prefixes=[])
        make.make(builddir=build.abspath(), args=['install'])
        
        self.failUnless(os.path.isfile(os.sep.join(
            install.abspath() + ['share', 'subdir', 'data', 'plainfile_data'])))
        self.failUnless(os.path.isfile(os.sep.join(
            install.abspath() + ['subdir', 'prefix', 'plainfile_prefix'])))

        pass
    pass        

if __name__ == '__main__':
    unittest.TextTestRunner().run(AutomakePlainfileBuildSuite())
    pass
