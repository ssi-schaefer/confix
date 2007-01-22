# Copyright (C) 2006 Joerg Faschingbauer

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

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.utils import const 
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.automake import bootstrap, configure, make

from libconfix.plugins.make.setup import MakeSetup
from libconfix.plugins.c.setup import DefaultCSetup

from libconfix.testutils.persistent import PersistentTestCase

import unittest
import sys
import os

class MakeBasicSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(MakeBasicTest('test'))
        pass
    pass

class MakeBasicTest(PersistentTestCase):
    def test(self):
        fs = FileSystem(path=self.rootpath())
        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())
        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())

        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("'+self.__class__.__name__+'")',
                              'PACKAGE_VERSION("1.2.3")']))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['CALL_MAKE_AND_RESCAN()']))
        source.add(
            name='Makefile',
            entry=File(lines=['all:',
                              '\tif test -e main.c; then echo "make being called twice"; exit 1; fi',
                              '\techo "// CONFIX:EXENAME(\'the_executable_generated_by_a_call_to_make\')" > main.cc',
                              '\techo "int main(void) {return 0;}" >> main.cc']))

        # during enlarge() we will call 'make' which expects the
        # Makefile being physically available in the physically
        # available directory, so flush it once ...
        fs.sync()
        
        package = LocalPackage(rootdirectory=source,
                               setups=[MakeSetup(),
                                       DefaultCSetup(short_libnames=False, use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()
        
        # ... and, for the rest of it, we need the automake input
        # files as well.
        fs.sync()

        bootstrap.bootstrap(
            packageroot=source.abspath(),
            path=None,
            use_libtool=False,
            use_kde_hack=False,
            argv0=sys.argv[0])
        configure.configure(
            packageroot=source.abspath(),
            builddir=build.abspath(),
            prefix=None,
            readonly_prefixes=None)
        make.make(
            builddir=build.abspath(),
            args=None)

        self.failUnless(os.path.isfile(os.sep.join(build.abspath()+['the_executable_generated_by_a_call_to_make'])))

        pass
    pass
                            
        
if __name__ == '__main__':
    unittest.TextTestRunner().run(MakeBasicSuite())
    pass

