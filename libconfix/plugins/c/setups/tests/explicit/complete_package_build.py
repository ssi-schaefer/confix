# Copyright (C) 2007 Joerg Faschingbauer

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

import complete_package

from libconfix.plugins.c.setups.explicit_setup import ExplicitCSetup
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.directory import Directory
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.hierarchy.explicit_setup import ExplicitDirectorySetup
from libconfix.core.automake import \
     bootstrap, \
     configure, \
     make
from libconfix.testutils.persistent import PersistentTestCase

import unittest
import sys

class CompletePackageBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(CompletePackageBuildTestWithLibtool('test'))
        self.addTest(CompletePackageBuildTestWithoutLibtool('test'))
        pass
    pass

class CompletePackageBuildTestBase(PersistentTestCase):
    def use_libtool(self):
        assert 0, 'abstract'
        pass
    def test(self):
        fs = FileSystem(path=self.rootpath())
        source = fs.rootdirectory().add(
            name='source',
            entry=complete_package.make_package_source(package_name=self.__class__.__name__))
        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())

        package = LocalPackage(rootdirectory=source,
                               setups=[ExplicitDirectorySetup(),
                                       ExplicitCSetup(use_libtool=self.use_libtool())])
        package.boil(external_nodes=[])
        package.output()
        fs.sync()

        bootstrap.bootstrap(
            packageroot=source.abspath(),
            use_libtool=self.use_libtool(),
            use_kde_hack=False,
            argv0=sys.argv[0])
        configure.configure(
            packageroot=source.abspath(),
            builddir=build.abspath(),
            prefix=None)
        make.make(
            builddir=build.abspath(),
            args=[])

        pass
    pass
        
class CompletePackageBuildTestWithoutLibtool(CompletePackageBuildTestBase):
    def use_libtool(self): return False
    pass

class CompletePackageBuildTestWithLibtool(CompletePackageBuildTestBase):
    def use_libtool(self): return True
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(CompletePackageBuildSuite())
    pass
