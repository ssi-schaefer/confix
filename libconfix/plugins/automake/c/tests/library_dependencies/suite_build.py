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

from dirstructure import DirectoryStructure

from libconfix.plugins.automake import bootstrap, configure, make
from libconfix.plugins.automake.repo_automake import AutomakePackageRepository

from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.filesys import scan

from libconfix.frontends.confix2.confix_setup import ConfixSetup

from libconfix.testutils.persistent import PersistentTestCase
from libconfix.testutils import makefileparser

import unittest
import sys
import os

class LibraryDependenciesBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(LibraryDependenciesBuildTest('test'))
        pass
    pass

class LibraryDependenciesBuildTest(PersistentTestCase):
    def test(self):
        dirstructure = DirectoryStructure(path=self.rootpath())

        # bootstrap&&configure&&build&&install packages in order
        first_local_package = LocalPackage(rootdirectory=dirstructure.first_source(),
                                           setups=[ConfixSetup(short_libnames=False, use_libtool=False)])
        first_local_package.boil(external_nodes=[])
        first_local_package.output()
        dirstructure.sync()
        bootstrap.bootstrap(
            packageroot=dirstructure.first_source().abspath(),
            path=None,
            use_kde_hack=False,
            argv0=sys.argv[0])
        configure.configure(
            packageroot=dirstructure.first_source().abspath(),
            builddir=dirstructure.first_build().abspath(),
            prefix=dirstructure.first_install().abspath(),
            readonly_prefixes=None)
        make.make(
            builddir=dirstructure.first_build().abspath(),
            args=['install'])


        second_local_package = LocalPackage(rootdirectory=dirstructure.second_source(),
                                            setups=[ConfixSetup(short_libnames=False, use_libtool=False)])
        second_local_package.boil(external_nodes=AutomakePackageRepository(prefix=dirstructure.first_install().abspath()).nodes())
        second_local_package.output()
        dirstructure.sync()
        bootstrap.bootstrap(
            packageroot=dirstructure.second_source().abspath(),
            path=None,
            use_kde_hack=False,
            argv0=sys.argv[0])
        configure.configure(
            packageroot=dirstructure.second_source().abspath(),
            builddir=dirstructure.second_build().abspath(),
            prefix=dirstructure.second_install().abspath(),
            readonly_prefixes=[dirstructure.first_install().abspath()])
        make.make(
            builddir=dirstructure.second_build().abspath(),
            args=['install'])


        third_local_package = LocalPackage(rootdirectory=dirstructure.third_source(),
                                           setups=[ConfixSetup(short_libnames=False, use_libtool=False)])
        third_local_package.boil(external_nodes=AutomakePackageRepository(prefix=dirstructure.first_install().abspath()).nodes() +\
                                 AutomakePackageRepository(prefix=dirstructure.second_install().abspath()).nodes())
        third_local_package.output()
        dirstructure.sync()
        bootstrap.bootstrap(
            packageroot=dirstructure.third_source().abspath(),
            path=None,
            use_kde_hack=False,
            argv0=sys.argv[0])
        configure.configure(
            packageroot=dirstructure.third_source().abspath(),
            builddir=dirstructure.third_build().abspath(),
            prefix=None,
            readonly_prefixes=[dirstructure.first_install().abspath(),
                               dirstructure.second_install().abspath()])
        make.make(
            builddir=dirstructure.third_build().abspath(),
            args=None)

        # so here, finally, go the tests.

        fs = scan.scan_filesystem(path=self.rootpath())

        first_library = fs.rootdirectory().find(dirstructure.first_install().relpath(self.rootpath())+['lib', 'libFirstPackage.a'])
        second_library = fs.rootdirectory().find(dirstructure.second_install().relpath(self.rootpath())+['lib', 'libSecondPackage.a'])
        third_library = fs.rootdirectory().find(dirstructure.third_build().relpath(self.rootpath())+['library', 'libThirdPackage_library.a'])
        third_exe_Makefile = fs.rootdirectory().find(dirstructure.third_build().relpath(self.rootpath())+['exe', 'Makefile'])
        self.failIf(first_library is None)
        self.failIf(second_library is None)
        self.failIf(third_library is None)
        self.failIf(third_exe_Makefile is None)

        elements = makefileparser.parse_makefile(third_exe_Makefile.lines())
        deps = makefileparser.find_list(name='ThirdPackage_exe_exe_DEPENDENCIES',
                                        elements=elements)
        self.failIf(deps is None)

        self.failUnless(os.sep.join(first_library.abspath()) in deps)
        self.failUnless(os.sep.join(second_library.abspath()) in deps)
        self.failUnless('$(top_builddir)/library/libThirdPackage_library.a' in deps)
        
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(LibraryDependenciesBuildSuite())
    pass
